# hooks/numpy_hook.py
def load_numpy(finder, module):
    """Find the numpy core extensions and ensure DLLs are properly located"""
    import os
    import numpy
    import glob
    import shutil

    # Include core packages
    finder.IncludePackage("numpy.core._multiarray_umath")
    finder.IncludePackage("numpy.core._multiarray_tests")
    finder.IncludePackage("numpy.core._rational_tests")
    finder.IncludePackage("numpy.core._struct_ufunc_tests")
    finder.IncludePackage("numpy.core._umath_tests")
    finder.IncludePackage("numpy.random")
    finder.IncludePackage("numpy.fft")
    finder.IncludePackage("numpy.linalg")

    # Get NumPy's directory
    numpy_dir = os.path.dirname(numpy.__file__)

    # Add DLLs from numpy to the include_files list
    for root, dirs, files in os.walk(numpy_dir):
        for file in files:
            if file.endswith('.dll') or file.endswith('.pyd'):
                source_path = os.path.join(root, file)
                # Determine relative path to maintain directory structure
                rel_dir = os.path.relpath(root, os.path.dirname(numpy_dir))
                target_dir = os.path.join("lib", rel_dir)
                finder.IncludeFiles(source_path, os.path.join(target_dir, file))

    # Look for MKL DLLs in typical locations
    python_dir = os.path.dirname(os.path.dirname(os.__file__))
    mkl_paths = [
        os.path.join(python_dir, 'Library', 'bin'),
        os.path.join(python_dir, 'DLLs'),
        os.path.join(os.path.dirname(numpy_dir), 'DLLs')
    ]

    # Include MKL DLLs if found
    for path in mkl_paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.startswith('mkl_') and file.endswith('.dll'):
                    finder.IncludeFiles(os.path.join(path, file), file)
