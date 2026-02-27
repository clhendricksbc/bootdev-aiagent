from functions.get_files_info import get_files_info

current_dir_result = get_files_info("calculator", ".")
print("Result for current directory:")
print(current_dir_result)
print("")

pkg_dir_result = get_files_info("calculator", "pkg")
print("Result for 'pkg' directory:")
print(pkg_dir_result)

bin_dir_result = get_files_info("calculator", "/bin")
print("Result for '/bin' directory:")
print(bin_dir_result)

prev_dir_result = get_files_info("calculator", "../")
print("Result for '../' directory:")
print(prev_dir_result)



