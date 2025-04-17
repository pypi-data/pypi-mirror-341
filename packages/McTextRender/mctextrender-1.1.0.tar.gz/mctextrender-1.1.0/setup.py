from setuptools import setup, find_packages

setup(
    name="McTextRender",
    version="1.1.0",
    description="Render Minecraft-style colored text in Python",
    author="Ventros",
    author_email="ventros.development@gmail.com",
    license = "MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["Pillow"],
    python_requires=">=3.8",
)