import streamlit as st
import pandas as pd
from io import StringIO
from stimulus_location import StimulusLocation


def analyze_file(file, calc, converter):
    """_summary_

    Args:
        file (_type_): _description_
    """    
    locs = {}

    resultsFilename = file.name.replace('_Log', 'Results')
    resultsOutput = []

    file_string = StringIO(file.getvalue().decode('utf-8')).read()
    first_lines = file_string.split('\n')[:3]
    
    resultsOutput.append(first_lines)

    log = pd.read_csv(file, skiprows=1)
    fp_fc_counter(log, resultsOutput)

    for row in log.iterrows(): 
        loc = (row[1][1], row[1][2])
        if (row[1][3] == 'Default'):

            if not loc in locs.keys():
                stim = StimulusLocation(row[1][0], row[1][1], row[1][2], resultsOutput)
                stim.logContrasts.append(row[1][5])
                stim.responses.append(row[1][7])

                locs.update({loc: stim})
            
            else:
                locs[loc].logContrasts.append(row[1][5])
                locs[loc].responses.append(row[1][7])

                if row[1][8] == 'Yes':
                    locs[loc].reversals.append(row[1][5])
        
        elif row[1][3] == 'FN':
            if not loc in locs.keys():
                stim = StimulusLocation(row[1][0], row[1][1], row[1][2], resultsOutput)
                stim.candidateFN.append(row[1][6])
                locs.update({loc: stim})
            else:
                locs[loc]
    
    for loc in locs.values():
        loc.finalize_location(calc, converter)

    FN_counter(locs, resultsOutput)
    output, heatmap = finalize_file(locs, resultsOutput)
    return resultsFilename, output, heatmap

def fp_fc_counter(log, resultsOutput):
    """_summary_

    Args:
        log (_type_): _description_
    """    

    fps = 0
    fix_checks = 0
    fix_loss = 0

    test_types = log['Test type'].to_numpy()
    responses = log['Responses'].to_numpy()

    trials = len(test_types)

    for i in range (len(log)):
        if test_types[i] == 'False Positive':
            fps += 1
        elif test_types[i] == 'Fixation check':
            fix_checks += 1
            if responses[i] == 'Yes':
                fix_loss += 1

    percent_FP = fps / trials

    if fix_checks > 0:
        percent_FL = fix_loss / fix_checks
    else:
        percent_FL = 0

    headers = ['Total trials', 'Percent false pos', 'Percent fixation loss']
    results = [f'{trials}', f'{percent_FP:.2f}', f'{percent_FL:.2f}']

    resultsOutput.append(headers)
    resultsOutput.append(results)

def FN_counter(locs, resultsOutput):
    """_summary_

    Args:
        locs (_type_): _description_
        resultsOutput (_type_): _description_
    """    
    FN_total = 0
    FN_missed = 0
    FN_candidates = 0

    for stim in locs.values():
        FN_total += stim.numFN
        FN_missed += stim.FNMissed
        FN_candidates += len(stim.candidateFN)

    percentFN = FN_missed/FN_total
    FNResults = ['False neg candidates: ', f'{FN_candidates}', 'False neg percent: ', f'{percentFN:.1f}']
    resultsOutput.append(FNResults)

def finalize_file(locs, resultsOutput):
    headers = ['Group', 'Location: x', 'Location: y', 'Log contrast', 'Responses', 'Reversal average (dB)', 'Weibull threshold (dB)']
    resultsOutput.append(headers)

    for loc in locs.values():
        loc.add_final_csv_line(resultsOutput)

    output = '\n'.join([', '.join(map(str, sublist)) 
                        for sublist in resultsOutput])

    heatmap = make_heatmap(resultsOutput)

    return output, heatmap

def make_heatmap(resultsOutput):
    #TODO
    pass
    

