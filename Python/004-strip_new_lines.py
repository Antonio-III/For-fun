with open("C:/Users/MICRO/For-fun/Python/text files/2020_job_titles.txt", "r") as opened_file:
    file_content = opened_file.readlines()

unique_job_titles = sorted( set( [ line.strip() for line in file_content ] ) )

print(unique_job_titles)