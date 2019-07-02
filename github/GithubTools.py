import subprocess
import git
import utils.BasicDirectoryOperations
import utils.DirectoriesOperations
import utils.FilesOperations
import os


def call_github(clone):
    service_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir + "/Files")
    if clone is True:
        subprocess.call("curlRequest.sh", shell=True)
    file = open(service_dir + "/services.txt", "r")
    fl = file.readlines()
    for x in fl:
        if x.__contains__("OSB") & x.__contains__("VS"):
            print('VirtualService --> ' + x)
            github_clone(x.rstrip('\n'), "OSB")
        elif x.__contains__("OSB") & x.__contains__("DS"):
            print('DataService --> ' + x)
            github_clone(x.rstrip('\n'), "OSB")
        elif x.__contains__("OSB") & x.__contains__("CS"):
            print('ConnectivityService --> ' + x)
            github_clone(x.rstrip('\n'), "OSB")
        elif x.__contains__("OSB"):
            print('OSB --> ' + x)
            github_clone(x.rstrip('\n'), "OSB")
        elif x.__contains__("SOA"):
            print('SOA --> ' + x)
            github_clone(x.rstrip('\n'), "SOA")
        # elif x.__contains__("BPM"):
        #     print('BPM --> ' + x)
        #     github_clone(x.rstrip('\n'))


def github_clone(name_repo, dir_path):
    dir_github = utils.FilesOperations.read_properties('GithubSection', 'github.path') + "\\" + dir_path
    name_repo_dir = utils.FilesOperations.read_properties('GithubSection', 'github.path') + "\\" + dir_path + "\\" \
                    + name_repo
    url = utils.FilesOperations.read_properties('GithubSection', 'github.endpoint') + name_repo + '.git'
    if utils.BasicDirectoryOperations.check_dirs(dir_github) is False:
        utils.BasicDirectoryOperations.create_dirs(dir_github)
    if utils.BasicDirectoryOperations.check_dirs(name_repo_dir) is False:
        git.Git(dir_github).clone(url)
    else:
        if 'Cibt-SOA-ManageOrganisation-BAS' in name_repo_dir:
            print('pasando del organisation')
        elif 'Cibt-SOA-ManageContactPoint-BAS' in name_repo_dir:
            print('pasando del ManageContactPoint')
        elif 'Cibt-SOA-ManageApplicationForm-BAS' in name_repo_dir:
            print('pasando del ManageApplicationForm')
            # error: unable to create file Cibt-SOA-ManageApplicationForm-BAS/SOA/Transformations/GetApplicationFormVariableDetail/Output_GetApplicationFormVariableDetailResp_GetReferenceDataResp_to_GetApplicationFormVariableDetailResp.xsl: Filename too long
            # error: unable to create file Cibt-SOA-ManageApplicationForm-BAS/SOA/Transformations/ValidateApplicationForm/XSLNonDeployedFiles/GetCountryCommitteeResp_GetCountryListResp_to_Output-Source-GetCountryCommitteeTerm_OutputVariable.GetCountryCommitteeTermRes.xml: Filename too long

        git.Git(name_repo_dir).pull()
    # utils.FilesOperations.read_properties('DigraphSection', 'digraph.sequence.path')


if __name__ == "__main__":
    # generator()
    call_github(False)
    # excel_simple_generator("Cibt-OSB-ManagePolicy-VS")