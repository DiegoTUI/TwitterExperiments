import sys
import signal
from util.trace import Trace
from twitter.location_stream import LocationStream

class _Main(object):
    "A class to run the main process of this script"

    twitterstream = None

    def usage(self):
        "Show command line help."

        Trace.error('Usage: twitterstream.py -sw 2.012,45.3232 -ne 3.119,48.8777 [fileout]')
        Trace.error('Launch a twitter stream client and send the result to an output')
        Trace.error('[fileout]: the file to dump the output. Stdout if omitted')
        Trace.error('  Parameters:')
        Trace.error('    --sw: longitude,latitude coordinates of the South West corner of the bounding box. Compulsory.')
        Trace.error('    --ne: longitude,latitude coordinates of the North East corner of the bounding box. Compulsory.')
        Trace.error('Example: python run_location_stream.py -sw -11.733398,35.763229 -ne 5.009766,42.970492')

    def keyboard_interrupt_handler(self, signal, frame):
        "handles KeyboardInterrupt signal"
        Trace.message("\nProcess interrupted by user. Exiting...")
        self.twitterstream.stop()
        sys.exit(0)

    def __init__(self, *argv):
        "Analyze the command line args and launch the Twitter location stream"

        southwest = None
        northeast = None
        output = sys.stdout
        # set KeyboardInterrupt signal handler
        signal.signal(signal.SIGINT, self.keyboard_interrupt_handler)
        #turn tuple into list
        argv = list(argv)
        # remove the first argument
        argv.pop(0)
        # iterate the list
        for argument in argv[:]:
            # look for southwest
            if argument == "-sw":
                try:
                    southwest = argv[argv.index("-sw") + 1]
                except IndexError:
                    self.usage()
                    return
                argv.remove("-sw")
                argv.remove(southwest)
            # look for northeast
            if argument == "-ne":
                try:
                    northeast = argv[argv.index("-ne") + 1]
                except IndexError:
                    self.usage()
                    return
                argv.remove("-ne")
                argv.remove(northeast)
        # check if argv was correct
        if southwest is None or northeast is None or len(argv) > 1:
            self.usage()
            return
        # check for output
        if len(argv) == 1:
            output = open(argv[0], "w")
        # launch the LocationStream
        self.twitterstream = LocationStream(southwest + "," + northeast)
        try:
            stream = self.twitterstream.start()
            Trace.message("Twitter stream started!!")
            Trace.message("Press ctrl+c to stop.")
        except:
            Trace.error("Raised exception: " + str(sys.exc_info()[0]))
            Trace.error("Stopping twitterstream")
            self.twitterstream.stop()
            return
        for line in stream:
            print >> output, line.strip()


if __name__ == '__main__':
    _Main(*sys.argv)
  
