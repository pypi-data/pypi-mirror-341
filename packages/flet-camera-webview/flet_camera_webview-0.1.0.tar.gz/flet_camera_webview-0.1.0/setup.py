from setuptools import setup, find_packages

setup(
    name="flet-camera-webview",
    version="0.1.0",
    description="Камера для Flet через WebView",
    author="Риженков Олександр",
    author_email="you@example.com",
    url="https://github.com/yourusername/flet_camera",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["flet", "flet_webview", "websockets"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
