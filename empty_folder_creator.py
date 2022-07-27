import os 

def generate_empty_folder(path):
    print(f'CREATING DIR WIH PATH  {path}')
    print("________________________________________________________________________________________________________________________________")

    if not os.path.exists(path):
        os.mkdir(path)
        print(f'Directory {path} created successfully')
    else:
        print('File Already Exist')


def create_empty_directories(file_type, statistic, league_name, year_start, year_end, need_year=True):
    path_current_directory = os.getcwd()

    directory_statistic = f'{file_type}/{statistic}'

    path_statistic = os.path.join(path_current_directory, directory_statistic)
    # generate folder for specific statistic
    generate_empty_folder(path_statistic)

    path_league = os.path.join(path_statistic, league_name)
    # generate folder for specific league
    generate_empty_folder(path_league)
    if need_year:
        for year in range(year_start, year_end):
            path_season =f'season_{year}_{year+1}'
            
            path_season = os.path.join(path_league, path_season)
            # generate folder for specific season
            generate_empty_folder(path_season)

if __name__ == '__main__':
    create_empty_directories('jsons','test_stat','epl', 2014, 2022)