#!/usr/bin/env python3

from __future__ import print_function

import argparse
import sys
import logging
from utils import *

def main():

    parser = argparse.ArgumentParser(prog='tilebatch', description="""Tile Batch a series of images in a given directory.
    exiftool must be available through PATH. The code sources the IMOD-linux.sh file before invoking any imod command line tools.""")
    parser.add_argument('folder', type=str, nargs=1,
                        help='a folder or more to monitor')
    parser.add_argument('-I','--imod-config', type=str, default="/sw/apps/imod/current/IMOD-linux.sh",
                        help='source this IMOD setup script before calling imod commands')
    parser.add_argument('-D','--dims', type=str, default="",
                        help='dimensions e.g. 2x3')
    parser.add_argument('-k','--keep-temporaries', action='store_true', default=False,
                        help='if set, all temporary files are kept')
    parser.add_argument('-l','--loglevel', action='store', default='info',
                        help='set the log level for the application')
    parser.add_argument('-L','--logfile', action='store', default='./tilebatch.log',
                        help='set the log level for the application (if no logfile name is given, the output is printed to the screen)')


    args = parser.parse_args()
    #
    #----------------------- configure the logger -----------------------
    #
    #taken from https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)

    if len(args.logfile) > 3:
        logging.basicConfig(filename=args.logfile,level=numeric_level, format='[%(levelname)8s] %(asctime)s %(message)s ', datefmt='%Y%m%d [%H:%M:%S]')
    else:
        logging.basicConfig(level=numeric_level, format='[%(levelname)8s] %(asctime)s %(message)s ', datefmt='%Y%m%d [%H:%M:%S]')

    current_load = check_load()
    if current_load > 5:
        logging.error("load on server too high (%f > 5). Exiting.",current_load)
        sys.exit(1)

    #
    #----------------------- search for folders that can be processed -----------------------
    #

    search_path = os.path.abspath(args.folder[0])

    if not os.path.exists(search_path):
        logging.error("search folder %s does not exist",search_path)
        sys.exit(1)

    logging.info("searching %s for files that end with *00[01].{tif,mrc}",search_path)

    tifre = re.compile('[0]+[01]\.tif')
    mrcre = re.compile('[0]+[01]\.mrc')
    single_mrcre = re.compile('\.mrc')


    #server is not under heavy load, let's start to work
    files_of_interest = []
    file_list_generator = os.walk(os.path.abspath(args.folder[0]))
    for root,dirs,files in os.walk(os.path.abspath(args.folder[0])):
        tif_files = glob.glob(os.path.join(root,"*.tif"))
        mrc_files = glob.glob(os.path.join(root,"*.mrc"))

        if len(tif_files) > 0:
            if has_been_processed(tif_files[0]):
                logging.info("candidate folder %s detected as already processed",root)
                continue

            for ff in files:
                temp_path = os.path.join(root,ff)
                if tifre.search(ff):
                    files_of_interest.append(temp_path)
                    break

        if len(mrc_files) > 0:
            if has_been_processed(mrc_files[0]):
                logging.info("candidate folder %s detected as already processed",root)
                continue

            if len(mrc_files) == 1:
                files_of_interest.append(mrc_files[0])
            else:
                for ff in files:
                    temp_path = os.path.join(root,ff)
                    if mrcre.search(ff):
                        files_of_interest.append(temp_path)
                        break

    if len(files_of_interest) == 0:
        logging.info("No candidate folders found with viable input data. Exiting.")
        sys.exit(0)
    #
    #----------------------- setup IMOD -----------------------
    #
    if os.path.exists(args.imod_config):
        source_shell_script(args.imod_config)
        output = subprocess.check_output("which blendmont", shell=True)
        logging.debug("sourced %s, using %s",args.imod_config,output)
    else:
        logging.error("unable to locate IMOD config shell script at %s. Exiting. ", args.imod_config)
        sys.exit(1)
    #
    #----------------------- start processing -----------------------
    #
    for initf in files_of_interest:
        path = os.path.dirname(initf)
        fname = os.path.split(initf)[-1]
        matched = re.search(tifre,fname)

        contains_tif = False
        contains_mrc = False
        contains_single_mrc = False

        if not matched:
            matched = re.search(single_mrcre,fname)
            if matched:
                contains_mrc = True
                contains_single_mrc = True
            else:
                logging.error("unable to match any regular expression against %s/%s. Skipping it!", path, fname)
                continue
        else:
            contains_tif = True

        inputfiles_wildcard = os.path.join(path,'*[0-9].tif')
        if not contains_tif:
            wildcard_expression = '*'
            # if not contains_single_mrc:
            #     wildcard_expression += '[0-9]'
            wildcard_expression += '.mrc'
            inputfiles_wildcard = os.path.join(path,wildcard_expression)


        inputfiles = sorted(glob.glob(inputfiles_wildcard))
        ninfiles = len(inputfiles)
        if not contains_tif:
            if ninfiles == 1:
                contains_mrc = False
                contains_single_mrc = True
                matched = re.search(single_mrcre,fname)
            if ninfiles > 1:
                contains_mrc = True
                contains_single_mrc = False
                matched = re.search(mrcre,fname)
        else:
            matched = re.search(tifre,fname)

        stem = fname[:matched.start()]
        logging.debug("%s/%s. tif: %i mrc: %i single_mrc: %i", path, fname, contains_tif,contains_mrc, contains_single_mrc)
        dimensions_equal = abs(math.sqrt(ninfiles) - math.floor(math.sqrt(ninfiles))) < 1e-7

        overlaps_path = os.path.join(path,stem+'_overlaps.txt')
        result_path = os.path.join(path,stem+'-Tiled.tif')

        if has_been_processed(initf):
        #if os.path.exists(overlaps_path) and os.stat(overlaps_path).st_size > 0 and os.path.exists(result_path):
            logging.warning("Folder %s as already processed (contains %s and %s). Skipping it!",path,result_path,overlaps_path)
            continue
        else:
            logging.info("Working on %s", os.path.join(path,stem))

        #----------------------- infer dimensions -----------------------
        #
        user_dims = args.dims

        parameter_file = os.path.join(path,'parameters.sh')
        dims = []
        if not os.path.exists(parameter_file):
            similar_to_parameter_file = glob.glob(os.path.join(path,'parameters*.sh'))
            if similar_to_parameter_file:
                logging.info("found %s instead of %s (using this for further processing)",similar_to_parameter_file[0],parameter_file)
                parameter_file = similar_to_parameter_file[0]


        if not os.path.exists(parameter_file):
            logging.debug("Folder %s does not contain <parameters.sh> (%s). Trying to detect dimensions of stack automagically.",path,parameter_file)
            if ninfiles > 1:
                if user_dims:
                    logging.debug("user given dimensions: %s", user_dims)
                    dims_string = user_dims.lower().split('x')
                    dims = [int(dims_string[0]), int(dims_string[1])]
                else:
                    dims=[int(math.sqrt(ninfiles))]*2
                    logging.debug("deduced dimensions from sqrt(number of input files) nfiles=%i dims_equal=%s",ninfiles,str(dimensions_equal))
            elif ninfiles == 1 and contains_single_mrc:
                if user_dims:
                    logging.debug("user given dimensions: %s", user_dims)
                    dims_string = user_dims.lower().split('x')
                    dims = [int(dims_string[0]), int(dims_string[1])]
                else:
                    dims = extract_dims_from_stack(inputfiles)
                    logging.debug("deduced dimensions from mrc stack metadata or filename",dims)
            else:
                logging.warning("Dimension detection failed. Skipping %s!\n%s\n%s",path,inputfiles,inputfiles_wildcard)
                continue
        else:
            logging.debug("deducing dimensions from %s",parameter_file)
            with open(parameter_file,'r') as pfile:
                lines = pfile.readlines()
                assert len(lines) >= 1
                segmentsr = re.compile('dim.=\d+')
                matched = re.findall(segmentsr," ".join(lines))
                assert len(matched) == 2
                segments = sorted(matched)
                #dimx always lands in dims[0], dimy should always be last
                dims = [ int(item.split('=')[-1]) for item in segments ]

        logging.info("found shape dimx=%i dimy=%i",dims[0],dims[1])
        #----------------------- produce overlap file -----------------------
        #
        cnt = 0
        if contains_tif:
            # we assume that the tif tiles are ordered in row-major
            # e.g. with 4x2 = 8 tiles, numbered from 0 to 7, the resulting montage should yield
            # | 0 | 1 | 2 | 3 |
            # | 4 | 5 | 6 | 7 |
            #

            #If the first line of tiles start at the top left and go to the right,
            # same for lines below etc...
            # ex:
            # 1 - 2 - 3
            # 4 - 5 - 6
            # 7 - 8 - 9

            # The command is:
            # edpiecepoint -output piecelist.txt -create 1 -pieces dimx, dimy -spacing
            # ox,-oy -add ox,oy,0

            # Where:
            #  - dimx is the number of tile in X
            #  - dimy is the number of tile in Y
            #  - ox is the tile width in pixel minus the overlap. ex: A tile of 2048
            # minus overlap of 25% : 2048-512 = 1536
            # -  -oy is the tile height in pixel minus the overlap. Here in negative:
            # -1536
# not correct anymore afer camera now has 4096x4096 pixels
            edpp_cmd = ["edpiecepoint",
                    "-output",overlaps_path,
                    "-create", str(1),
                    "-pieces", "%i, %i" % tuple(dims),
                    "-spacing","%i,%i" % (3686,-3686),
                    "-add", "%i,%i,0" % (3686,3686)
            ]
            logging.debug("[F30/T12 TIF] creating %s from %s",overlaps_path,str(edpp_cmd))
            edpp_out = subprocess.Popen(edpp_cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdo, stde  = edpp_out.communicate()

            if not edpp_out.returncode == 0:

                logging.error("command %s returned:\n%s\nCancelling processing.", edpp_cmd, stdo )
                continue

        elif contains_mrc:

            ## If the tiling is organized in column, starting bottom left and going up
            ## (like tiling in SerialEM)
            ##
            ## 3 - 6 - 9
            ## 2 - 5 - 8
            ## 1 - 4 - 5
            ##
            ## edpiecepoint -output piecelist.txt -create 1 -pieces dimx,dimy -spacing
            ## ox,oy -columns
            ##
            edpp_cmd = ["edpiecepoint",
                    "-output",overlaps_path,
                    "-create", str(1),
                    "-pieces", "%i, %i" % tuple(dims),
                    "-spacing","%i,%i" % (1536,1536),
                    "-add", "%i,%i,0" % (1536,1536)
            ]
            logging.debug("[F30 MRC] creating %s from %s",overlaps_path,str(edpp_cmd))
            edpp_out = subprocess.Popen(edpp_cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdo, stde  = edpp_out.communicate()

            if not edpp_out.returncode == 0:

                logging.error("command %s returned:\n%s\nCancelling processing.", edpp_cmd, stdo )
                continue

            # for j in range(dims[0]):#x index
            #     for i in range(dims[-1]):#y index
            #         offset_x = j*1535
            #         offset_y = (dims[-1] - i - 1)*1535

            #         logging.debug("[F30 MRC] x=%i y=%i is assigned file %s",offset_x,offset_y,inputfiles[cnt])
            #         overlaps_txt.write("%i %i 0\n" % (offset_x,offset_y))
            #         cnt += 1
        elif contains_single_mrc:
            # we assume that the mrc tiles stored in the stack I was given are ordered in inverse column-major
            # e.g. with 4x2 = 8 tiles, numbered from 0 to 7, the resulting montage should yield
            # | 1 | 3 | 5 | 7 |
            # | 0 | 2 | 4 | 6 |
            # This is what I deduced from calling mrc2tif on the stack and manually aligning the tifs that I got
            # However, experimenting the indices below indicates plain column-major ordering
            overlaps_txt = open(overlaps_path,'w')
            for j in range(dims[0]):#x index
                for i in range(dims[-1]):#y index
                    offset_x = j*3686
                    #offset_y = (dims[-1] - i - 1)*1535
                    offset_y = i*3686
                    logging.debug("[F30 MRC] x=%i y=%i is assigned file %s:%i",offset_x,offset_y,inputfiles[0],cnt)
                    overlaps_txt.write("%i %i 0\n" % (offset_x,offset_y))
                    cnt += 1
            overlaps_txt.close()

        #----------------------- run IMOD tools -----------------------
        #
        blendmont_imin = os.path.join(path,stem+'.st') if ninfiles > 1 else inputfiles[0]
        blendmont_imout = os.path.join(path,stem+'_blended.mrc')
        rt_path = os.path.join(path,stem+'.rt')

        if contains_tif:
            tif2mrc_cmd = ["tif2mrc"]
            tif2mrc_cmd.extend(inputfiles)
            tif2mrc_cmd.append(blendmont_imin)
            logging.debug(" ".join(tif2mrc_cmd))
            tif2mrc_out = subprocess.Popen(tif2mrc_cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdo, stde  = tif2mrc_out.communicate()

            if not tif2mrc_out.returncode == 0:

                logging.error("command %s returned:\n%s\nCancelling processing.", tif2mrc_cmd, stdo )
                continue

            assert os.path.exists(blendmont_imin) and os.stat(blendmont_imin).st_size > 0
        elif not contains_single_mrc:
            newstack_cmd = ["newstack"]
            newstack_cmd.extend([ os.path.split(item)[-1] for item in inputfiles ])
            newstack_cmd.append(os.path.split(blendmont_imin)[-1])
            logging.debug(" ".join(newstack_cmd))
            newstack_out = subprocess.Popen(newstack_cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd = path)
            stdo, stde  = newstack_out.communicate()

            if not newstack_out.returncode == 0:

                logging.error("command %s failed with \n%s\nCancelling processing.", newstack_cmd, stdo )
                continue

            assert os.path.exists(blendmont_imin) and os.stat(blendmont_imin).st_size > 0

        #blendmont -imin F30-3x3.mrc -imout F30-3x3.mrc -mode 1 -float -plin F30-3x3_overlaps.txt -rootname F30-3x3.rt
        bm_cmd= ["blendmont",
                 "-imin",os.path.split(blendmont_imin)[-1],
                 "-imout",os.path.split(blendmont_imout)[-1],
                 "-mode","1",
                 "-float",
                 "-plin",os.path.split(overlaps_path)[-1],
                 "-rootname",stem+'.rt',
                 "-very"]


        logging.debug("running '%s' with cwd=%s"," ".join(bm_cmd), path)

        bm_out = subprocess.Popen(bm_cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd = path)
        stdo, stde  = bm_out.communicate()

        if not bm_out.wait() == 0:
            logging.error("command %s failed with \n%s\nCancelling processing.", " ".join(bm_cmd), stdo )
            continue
        else:
            assert os.path.exists(blendmont_imout) and os.stat(blendmont_imout).st_size > 0

        if not args.keep_temporaries:
            [ os.remove(item) for item in glob.glob(rt_path+".*") ]
            if not contains_single_mrc:
                [ os.remove(item) for item in glob.glob(blendmont_imin+"*" ) ]

        ## *************************************
	    # blendmont_imout = " -P " + blendmont_imout
        mrc2tifcmd= ["mrc2tif", "-P", blendmont_imout,result_path]
        logging.debug(" ".join(mrc2tifcmd))

        #
	    # mrc2tifcmd = " -P " + mrc2tifcmd
        mrc2tifout = subprocess.Popen(mrc2tifcmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdo, stde  = mrc2tifout.communicate()

        if not mrc2tifout.wait() == 0:
            logging.error("command %s returned:\n%s\nCancelling processing.", mrc2tifcmd, stdo )
            continue

        assert os.path.exists(result_path) and os.stat(result_path).st_size > 0


        #----------------------- add meta data -----------------------
        #
        if contains_tif:
            size_result_path = os.stat(result_path).st_size
            exift_cmd = ["exiftool"]
            if not args.keep_temporaries:
                exift_cmd.append("-overwrite_original_in_place")
            exift_cmd.extend(["-tagsFromFile",initf,result_path])
            logging.debug(" ".join(map(str, exift_cmd)))
            exift_out = subprocess.Popen(exift_cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdo, stde  = exift_out.communicate()

            if not exift_out.wait() == 0:
                logging.error("command %s returned:\n%s\nCancelling processing.", exift_cmd, stdo )
                continue

            assert size_result_path != os.stat(result_path).st_size
            os.remove(blendmont_imout)

            logging.info("Finishing %s", result_path)

    logging.info("Done.")
    sys.exit(0)



if __name__ == '__main__':
    main()
