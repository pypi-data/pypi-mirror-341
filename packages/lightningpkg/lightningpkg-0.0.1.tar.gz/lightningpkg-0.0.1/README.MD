
# Option 1 - Building Python Wheels

## Prepare building tools

    pip install --upgrade setuptools wheel twine

## Preparing Project layout

    mypackage/
        src/
            __init__.py
            module1.py
            module2.py
        setup.py
        README.md
        LICENSE

### Preparing the setup.py

An Example.

    from setuptools import setup, find_packages
    
    setup (
        name='src',
        version='0.0.1',
        description='It is a wine quality prediction package',
        author='Juhe',
        author_email='juhe.terence@gmail.com',
        packages=find_packages(),
        license='MIT'
    )

### Build the pacakge

    python setup.py bdist_wheel

Output:
    
[dist](dist)/[src-0.0.1-py3-none-any.whl](dist/src-0.0.1-py3-none-any.whl)


# Reference

https://medium.com/@jonathan.hoffman91/a-step-by-step-guide-to-building-python-wheels-4ed8160809a2

