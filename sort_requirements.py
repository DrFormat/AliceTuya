requirements_files = ['requirements.txt', 'requirements-dev.txt']

for requirements_file in requirements_files:
    requirements = open(requirements_file, 'r')
    content = requirements.read().splitlines()
    content = list(set(content))
    content.sort(key=lambda y: y.lower())
    content = '\n'.join(content)

    requirements = open(requirements_file, 'w')
    requirements.write(content)
    requirements.close()
