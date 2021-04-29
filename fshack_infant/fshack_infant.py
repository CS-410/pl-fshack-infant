#!/usr/bin/env python
#
# fshack_infant DS ChRIS plugin app
#
# (c) 2016-2020 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import  os
import  sys
import  subprocess
import  glob

sys.path.append(os.path.dirname(__file__))

# import the Chris app superclass
from    chrisapp.base import ChrisApp
import  pudb

Gstr_title = """
  __     _                _      _        __            _   
 / _|   | |              | |    (_)      / _|          | |  
| |_ ___| |__   __ _  ___| | __  _ _ __ | |_ __ _ _ __ | |_ 
|  _/ __| '_ \ / _` |/ __| |/ / | | '_ \|  _/ _` | '_ \| __|
| | \__ \ | | | (_| | (__|   <  | | | | | || (_| | | | | |_ 
|_| |___/_| |_|\__,_|\___|_|\_\ |_|_| |_|_| \__,_|_| |_|\__|
"""

Gstr_synopsis = """
    NAME
       fshack_infant.py
       
    SYNOPSIS
        python fshack_infant.py
            [-i|--inputFile <file>]
            [-o|--outputFile <file>]
            [-e|--exec <command>]
            [-a|--args <arguments>]
            [-h|--help]
            [--man]
            [--json]
            [--savejson <directory>]
            [--meta]
            [-v|--verbosity <level>]
            [--version]
            <inputDir> <outputDir>

    DESCRIPTION
        This ChRIS DS plugin contains a complete Infant FreeSurfer distribution.
        Not all FreeSurfer internal applications are exposed at the plugin level,
        however. Currently, the following Infant FreeSurfer applications are
        directly accessible from the plugin CLI:
            * `recon-all`
            * `mri_convert`
            * `mri_info`
            * `mris_info`
        This plugin is meant to demonstrate certain design patterns and provide
        some utility for running Infant FreeSurfer within the context of ChRIS.
        It is not meant nor intended to be a canonical Infant FreeSurfer ChRIS
        plugin -- as explicitly indicated by the name, FreeSurfer 'hack'.
        Colloquially, this plugin is also known as `f-shack-infant`.
        
    ARGS
        [-i|--inputFile <file>]
        Input file to process. In most cases, this is typically a DICOM file or
        a NIfTI volume, but is also very dependent on context. This file exists
        within the explictly provided <inputDir> directory. If specified as a
        string that starts with a period character, then <inputDir> will be
        examined and the first `ls`-ordered file in the glob pattern
                        '*' + <inputFileWithoutPeriod> + '*'
        will be assigned as the <file> argument. For example, specifying '.0001'
        will assign the first file that satisfies the glob '*0001*'.
        
        [-o|--outputFile <file>]
        Output file/directory name to use within the <outputDir> directory. Note
        the actual meaning of this usage is contextual to the particular FS app.
        For example, in the case of `recon-all`, this argument maps to the
                                -s|--subjectID <ID>
        flag. It should also be noted that the <file> string is used to prepend
        many of the CLI -stdout -stderr and -returncode filenames.
        
        [-e|--exec <command>]
        Specifies the FreeSurfer command within the plugin/container to execute.
        As stated in the description, it must be noted that only a few of the
        Infant FreeSurfer apps are currently exposed!
        
        [-a|--args <arguments>]
        Optional string of additional arguments to 'pass through' to the FS app.
        The design pattern of this plugin is to provide, somewhat blindly, all
        the CLI arguments for a single app specified by the `exec` flag. To this
        end, all the arguments for a given supported internal FreeSurfer app are
        themselves specified at the plugin level with this flag. These arguments
        MUST be enclosed within single quotes (to protect them from the shell)
        AND curly brackets (to protect from Python).

        If the FS app does not require additional CLI arguments, then this flag
        can be safely omitted.
        
        [-h|--help]
        If specified, show help message.
        
        [--man]
        If specified, print (this) man page.
        
        [--json]
        If specified, show JSON representation of app.
        
        [--savejson <dir>]
        If specified, save JSON representation file to <dir>.
        
        [--meta]
        If specified, print plugin metadata.
        
        [--version]
        If specified, print version number.
"""


class Fshack_infant(ChrisApp):
    DESCRIPTION             = 'This app houses a complete Infant FreeSurfer distro and exposes some Infant FreeSurfer apps at the level of the plugin CLI.'
    AUTHORS                 = 'FNNDSC / CS410 (dev@babyMRI.org)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A quick-and-dirty attempt at hacking an Infant FreeSurfer ChRIS plugin'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DOCUMENTATION           = 'https://github.com/CS-410/pl-fshack-infant'
    VERSION                 = '1.0.2'
    ICON                    = ''  # URL of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1   # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1   # Override with integer value
    MAX_CPU_LIMIT           = ''  # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = ''  # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = ''  # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = ''  # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0   # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0   # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        """
        self.add_argument("-a", "--args",
                          help      = "Arguments to pass to Infant FS app",
                          type      = str,
                          dest      = 'args',
                          optional  = True,
                          default   = "")
        self.add_argument("-e", "--exec",
                          help      = "Infant FS app to run",
                          type      = str,
                          dest      = 'exec',
                          optional  = True,
                          default   = "recon-all")
        self.add_argument("-i", "--inputFile",
                          help      = "input file (use .<ext> to find and use the first file with that extension)",
                          type      = str,
                          dest      = 'inputFile',
                          optional  = True,
                          default   = "")
        self.add_argument("-o", "--outputFile",
                          help      = "output file",
                          type      = str,
                          dest      = 'outputFile',
                          optional  = True,
                          default   = "run")

    def job_run(self, str_cmd):
        """
        Running some CLI process via python is cumbersome. The typical/easy
        path of
                            os.system(str_cmd)
        is deprecated and prone to hidden complexity. The preferred
        method is via subprocess, which has a cumbersome processing
        syntax. Still, this method runs the `str_cmd` and returns the
        stderr and stdout strings as well as a returncode.
        Providing readtime output of both stdout and stderr seems
        problematic. The approach here is to provide realtime
        output on stdout and only provide stderr on process completion.
        """
        d_ret = {
            'stdout':       "",
            'stderr':       "",
            'returncode':   0
        }

        localEnv    = os.environ.copy()
        localEnv["SUBJECTS_DIR"] = self.options.outputdir
        p = subprocess.Popen(
                    str_cmd.split(),
                    stdout      = subprocess.PIPE,
                    stderr      = subprocess.PIPE,
                    env         = localEnv
                    )

        # Realtime output on stdout
        str_stdoutLine  = ""
        str_stdout      = ""
        while True:
            stdout      = p.stdout.readline()
            if p.poll() is not None:
                break
            if stdout:
                str_stdoutLine = stdout.decode()
                print(str_stdoutLine, end = '')
                str_stdout      += str_stdoutLine
        d_ret['stdout']     = str_stdout
        d_ret['stderr']     = p.stderr.read().decode()
        d_ret['returncode'] = p.returncode
        print('\nstderr: \n%s' % d_ret['stderr'])
        return d_ret

    def job_stdwrite(self, d_job, options):
        """
        Capture the d_job entries to respective files.
        """
        for key in d_job.keys():
            with open(
                '%s/%s-%s' % (options.outputdir, options.outputFile, key), "w"
            ) as f:
                f.write(str(d_job[key]))
                f.close()
        return {
            'status': True
        }

    def inputFileSpec_parse(self, options):
        """
        Parse the inputFile value and possibly trigger some contentual
        behaviour. Specifically, if the inputFile spec starts with a
        period, '.', then search the inputDir for the first file with
        that substring and assign that file as inputFile.
        Modify the options variable in place.
        """
        str_thisDir:    str     = ''
        str_pattern:    str     = ''
        l_files:        list    = []
        if options.inputFile.startswith('.'):
            str_pattern     = options.inputFile[1:]
            str_thisDir     = os.getcwd()
            os.chdir(options.inputdir)
            l_files         = glob.glob('*' + str_pattern + '*')
            if len(l_files):
                options.inputFile = l_files[0]
            os.chdir(str_thisDir)

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        global str_cmd
        print(Gstr_title)
        print('Version: %s' % self.get_version())
        for k, v in options.__dict__.items():
            print("%20s:  -->%s<--" % (k, v))

        self.options = options

        self.inputFileSpec_parse(options)

        if not options.args.startswith('{') and not options.args.endswith('}'):
            options.args = ''
        else:
            options.args = options.args[1:-1]

        str_FSbinDir = '/usr/local/freesurfer/bin'
        str_cmd = ""
        if options.exec == 'recon-all':
            str_cmd = '%s/%s -i %s/%s -subjid %s/%s %s ' % \
                      (str_FSbinDir,
                       options.exec, options.inputdir, options.inputFile,
                       options.outputdir, options.outputFile, options.args)

        if options.exec == 'mri_convert':
            str_cmd = '%s/%s %s/%s  %s/%s %s ' % \
                      (str_FSbinDir,
                       options.exec, options.inputdir, options.inputFile,
                       options.outputdir, options.outputFile, options.args)

        if options.exec == 'mri_info':
            str_cmd = '%s/%s %s/%s %s ' % \
                      (str_FSbinDir,
                       options.exec, options.inputdir, options.inputFile,
                       options.args)

        if options.exec == 'mris_info':
            str_cmd = '%s/%s %s/%s %s' % \
                      (str_FSbinDir,
                       options.exec, options.inputdir, options.inputFile,
                       options.args)

        # Run the job and provide realtime stdout
        # and post-run stderr
        self.job_stdwrite(
            self.job_run(str_cmd), options
        )

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Fshack_infant()
    chris_app.launch()
