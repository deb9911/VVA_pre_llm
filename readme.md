<h2>Vani Virtual Assistant</h2>
<br>
<bd>"V" = Virtually</bd>
<br>
<bd>"A" = Analysed</bd>
<br>
<bd>"N" = Neural</bd>
<br>
<bd>"I" = Implementation</bd>

<br>Requirements for setting up</br>

req.txt

``.\env\Scripts\activate.bat``

``pip install -r req.txt``


**Simple execution way is, executing the build executable.**

``C:\Users\{username}\Documents\Jarin_Virtual_assistant\env\Scripts\python.exe C:/Users/{username}/Documents/Jarin_Virtual_assistant/jarine_va.py``


<h3>Navigate to executable package</h3>

``Under Dist directory > jarine_va > jarine_va.exe``

<h3>executable command</h3>
``  dist\jarine_va\jarine_va.exe  ``

<h3> Important dependency for build: PocketSphinx set up</h3>
To avoid Pre- & Post-set up complexity specially for pocketSphinx. 
Into the distribution, 

I'm adding a .bat for windows system support. 
Later will add for Lixux or Posix based backed up too.  

```git clone --recursive https://github.com/cmusphinx/pocketsphinx-python/```

```cd pocketsphinx-python```

```python setup.py install```

<bd>**=======================================================**</bd>


[vva_premier1.mp4](..%2F..%2FDownloads%2Fvva_premier1.mp4)

<h2>Changelog</h2>
<br>Ver: 4.0.1</br>
* Interpreter updated.
* Package updated
* Add dagster for data & process flow visualize. 
* Add multiple keywords. 
* Add integration for another services. 

