import subprocess
import os

# by Bhavin Joshi

home = os.getenv('HOME')

def callcsp(isedfile, metallicity, tauV, mu, tau, dust='y', sfh='1', recycle='y', ep='0.1', tcut='13.8'):

    # open the process to be executed, i.e. csp_galaxev, in this case
    # first arg is the location of the process as a list
    # stdin and stdout are the location of the input and output respectively. 
    # I think by specifying this to be subprocess.PIPE I'm telling it to direct the input and output in the default way
    start = subprocess.Popen([home + '/Documents/GALAXEV_BC03/bc03/src/csp_galaxev'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # in this case the process to be executed needs to know the name of the output file to write to
    # over here I'm choosing to name the file based on the parameters I'll be passing to my process
    # (the specifics in this line below aren't that important)
    output = "bc2003_hr_" + metallicity + "_tauV" + str(int(tauV*10)) + "_csp_tau" + str(int(float(str(tau)[0:6])*10000)) + "_salp"
    print output

    # execute the process
    # start.communicate() will communicate the input parameters that the process needs to be executed
    # in this case I'm passing the parameters that are required by csp_galaxev 
    params = start.communicate(os.linesep.join([isedfile, dust, str(tauV), str(mu), sfh, str(tau), recycle, ep, tcut, output]))

    # find if the process was properly executed
    start.poll()
    
    return None
