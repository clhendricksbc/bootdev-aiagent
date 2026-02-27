from functions.get_file_content import get_file_content

lorum_result = get_file_content("calculator", "lorem.txt")
print("Result for lorum.txt")
print(lorum_result)
print("")

main_result = get_file_content("calculator", "main.py")
print("Result for main.py")
print(main_result)
print("")

print("Result for pkg/calculator.py")
print(get_file_content("calculator", "pkg/calculator.py"))
print("")

print("Result for /bin/cat")
print(get_file_content("calculator", "/bin/cat"))
print("")

print("Result for pkg/does_not_exist.py")
print(get_file_content("calculator", "pkg/does_not_exist.py"))


