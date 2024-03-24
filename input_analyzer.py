import streamlit as st
import pandas as pd
from io import StringIO
from stimulus_location import StimulusLocation


def analyze_file(file, calc, converter):
    """Save file information to StimulusLocation objects in order
        to generate results files

    Args:
        file (UploadedFile): A file uploaded via the streamlit file uploader 
            containing the test log data from a VFT
        calc (WeibullCalculator): Global WeibullCalculator object
        converter (UnitConversions): Global UnitConverter object

    Returns:
        string, list, plot: 
            The filename for the results file that corresponds with the
                inputted log
            A list of lists of strings to be turned into a csv for the
                results file
            A heatmap containing the results from the VFT and reliability
                indices
    """   
    locs = {}

    #Generate the file name for the results file
    resultsFilename = file.name.replace('_Log', 'Results')
    resultsOutput = []

    #Copy the first 3 lines of the log file into results
    file_string = StringIO(file.getvalue().decode('utf-8')).read()
    first_lines = file_string.split('\n')[:3]
    resultsOutput.append(first_lines)

    #Store the log file as a dataframe and count false pos and fix. checks
    log = pd.read_csv(file, skiprows=1)
    fp_fc_counter(log, resultsOutput)

    #Iterate through each row to add data to Stimulus Location classes
    for row in log.iterrows(): 
        #Set the location as the x, y coordinate
        loc = (row[1][1], row[1][2])

        if (row[1][3] == 'Default'):
            
            #For default rows, add the location to the dictionary
            #if not already added
            if not loc in locs.keys():

                #Create a new stimulus location and add log contrasts and responses
                stim = StimulusLocation(row[1][0], row[1][1], row[1][2], resultsOutput)
                stim.logContrasts.append(row[1][5])
                stim.responses.append(row[1][7])

                #Add to dictionary
                locs.update({loc: stim})
            
            else:
                #Otherwise, add log contrast, responses, and reversal if needed
                locs[loc].logContrasts.append(row[1][5])
                locs[loc].responses.append(row[1][7])

                if row[1][8] == 'Yes':
                    locs[loc].reversals.append(row[1][5])
        
        elif row[1][3] == 'FN':
            #For FN trials, add the location to the dictionary
            #if not already added
            if not loc in locs.keys():
                #Create a stimulus location and add response to candidate FN
                stim = StimulusLocation(row[1][0], row[1][1], row[1][2], resultsOutput)
                stim.candidateFN.append(row[1][7])
                locs.update({loc: stim})
            else:
                #Otherwise, just add response to existing location
                locs[loc].candidateFN.append(row[1][7])
    
    #Once all rows have been processed, finalize the location
    #by running estimating weibull threshold
    for loc in locs.values():
        loc.finalize_location(calc, converter)

    #Get total true FNs and responses
    FN_counter(locs, resultsOutput)

    #Finalize results file and output and return
    output, heatmap = finalize_file(locs, resultsOutput)
    return resultsFilename, output, heatmap

def fp_fc_counter(log, resultsOutput):
    """Count the number of false positives and the fixation checks
        from a log file

    Args:
        log (Pandas DataFrame): A dataframe storing the information from
            the VFT test log
        resultsOutput (list): A list of lists of strings to be outputted
            into the results csv file, modified in place
    """ 

    #Initialize variables
    fps = 0
    fix_checks = 0
    fix_loss = 0

    test_types = log['Test type'].to_numpy()
    responses = log['Responses'].to_numpy()

    trials = len(test_types)

    #Add up all false positives, fixation checks, and fixation losses
    for i in range (len(log)):
        if test_types[i] == 'False Positive':
            fps += 1
        elif test_types[i] == 'Fixation check':
            fix_checks += 1
            if responses[i] == 'Yes':
                fix_loss += 1

    #Get percent false positive
    percent_FP = fps / trials

    #Get percent fixation loss / total fixation checks
    #Manually set as zero if no checks to avoid div by 0 error
    if fix_checks > 0:
        percent_FL = fix_loss / fix_checks
    else:
        percent_FL = 0

    #Generate headers and strings of the output values and add to the list
    headers = ['Total trials', 'Percent false pos', 'Percent fixation loss']
    results = [f'{trials}', f'{percent_FP:.2f}', f'{percent_FL:.2f}']

    resultsOutput.append(headers)
    resultsOutput.append(results)

def FN_counter(locs, resultsOutput):
    """Count the number of false negatives from a VFT log file

    Args:
        locs (list): A list of populated StimulusLocation objects
        resultsOutput (list): A list of lists of strings to be outputted
            into the results csv file, modified in place
    """  

    #Initialize variables  
    FN_total = 0
    FN_missed = 0
    FN_candidates = 0

    #For each location, add the total number of false negatives,
    # Total number missed, and total total number of FN trials
    for stim in locs.values():
        FN_total += stim.numFN
        FN_missed += stim.FNMissed
        FN_candidates += len(stim.candidateFN)

    #Add the percent false negatives missed and the total number
    #Of candidates to the results output
    #TODO: ask chris about output: FN or otherwise
    percentFN = FN_missed/FN_total
    FNResults = ['False neg candidates: ', f'{FN_candidates}', 'False neg percent: ', f'{percentFN:.1f}']
    resultsOutput.append(FNResults)

def finalize_file(locs, resultsOutput):
    """Finalize the results file using the stimulus location objects

    Args:
        locs (list): A list of StimulusLocation objects in the VFT
        resultsOutput (list): A list of lists of strings to be outputted
            into the results CSV

    Returns:
        tuple: First: One string representation of the results output file
            as a csv
                Second: The heatmap representation of the VFT results
    """    

    #Add all the results headers
    headers = ['Group', 'Location: x', 'Location: y', 'Log contrast', 'Responses', 'Reversal average (dB)', 'Weibull threshold (dB)']
    resultsOutput.append(headers)

    #Add the final line from each stimulus location, including threshold
    for loc in locs.values():
        #TODO: Add a dunder compare method to sort list
        loc.add_final_csv_line(resultsOutput)

    #Generate the csv string representation of the results output
    output = '\n'.join([', '.join(map(str, sublist)) 
                        for sublist in resultsOutput])

    #Generate the heatmap
    heatmap = make_heatmap(resultsOutput)

    return output, heatmap

def make_heatmap(resultsOutput):
    #TODO
    pass
    

