<html>
<body>

<h1>ReviTab Documentation</h1>

<h2>Table of contents</h2>

<ul>
    <li><a href="#Introduction">Introduction</a></li>
    <li><a href="#Guide-dutilisation">User guide</a>
        <ul>
            <li><a href="#Installation-de-lapplication">1. Installing the app</a></li>
            <li><a href="#Fonctionnalités-de-lapplication">2. App Features</a>
                <ul>
                    <li><a href="#Interface-generale">2.1 General Interface</a></li>
                    <li><a href="#Edition-de-fichier-CSV">2.2 Editing CSV files</a></li>
                    <li><a href="#Creation-dexercices">2.3 Create exercise</a></li>
                    <li><a href="#Mode-exercice">2.4 Exercise mode</a></li>
                    <li><a href="#Parametres">2.5 Configure the application</a></li>
                    <li><a href="#Licences-et-user-guide">2.6 Licenses and User Guide</a></li>
                </ul>
            </li>
            <li><a href="#Liste-raccourcis">Appendix: List of Shortcuts</a></li>
        </ul>
    </li>
</ul>


<h2 id="Introduction">Introduction</h2>

<p>ReviTab is a Windows application that lets you edit CSV files, practice with them, and export them as PDF tables.</p>

<h2 id="Guide-dutilisation">User guide</h2>

<h3 id="Installation-de-lapplication">1. Installing the app</h3>

<p>ReviTab is an application compiled in one-file mode using PyInstaller : 
    that is, the application consists of a single document.
    It requires no additional installation. The application can be stored anywhere on the computer.
</p>
<p>The first time you use the program, a folder named <code>.revitab</code> will be created. 
    This directory contains the application's configuration file named <code>config.toml</code>. It also contains the language file.
    (defult : <code>english.toml</code> and <code>francais.toml</code>). You can add your own language files, 
    but be careful to the names of the file elements' keys (TIP : Copy one of the default files and change the text).
    If th folder is deleted, removed or renamed, it will be automatically recreated with the app's default settings.</p>

<h3 id="Fonctionnalités-de-lapplication">2. App Features</h3>

<h4 id="Interface-generale">2.1 General Interface</h4>

<p>ReviTab uses a tabbed interface. This means that you can open multiple files at the same time andd create multiple exercises.
   The toolbar changes dependig on which tab is open (Home, Documentation, Exercise, Edit). 
   Therefore, the features available to you vary, depending on which tab is open.
</p>

<h4 id="Edition-de-fichier-CSV">2.2 Editing CSV files</h4>

<p>To open a CSV file, go to the <code>File</code> menu, and select <code>Open...</code> (shortcut : <code>Ctrl+O</code>). 
    A window will open, allowing you to select a file to open. 
    You can only open CSV files.</p>
<p>You can also create new file,  
    by selecting the <code>New</code> option from the <code>File</code> menu (shotcut : <code>Ctrl+N</code>).</p>
<p>The selected file is displayed as a table. 
    You can add or remove rows and columns as well as change the column headers.</p>
<p>To save the file, click the save icon in the toolbar or go to <code>File</code>, <code>Save</code> (shortcut <code>Ctrl+S</code>). 
    If this is a new file, a window will appear asking you to select a location for the CSV file. 
    If the file has been modified but not saved, you will be asked to confirm before closing the tab or the application.</p>
<p>You can export the table to a PDF file, by selecting the <code>Export to PDF</code> option (shortcut <code>Ctr+P</code>). When exporting, you can choose the title displayed at the top of the document, and decide wether a evaluation-like header is shown. This feature can also be used with exercises.</p>
<p>To insert an ß, use the shortcut <code>Ctrl+Shift+S</code>.</p>
<p>You can also create exercises from open files (see next section)</p>

<h4 id="Creation-dexercices">2.3 Create exercise</h4>

<p>ReviTab allows you to generate exercises from CSV files.
    To create an exercise, you must first open the file you want to practice with,
    then, click the <code>Practice</code> button (shortcut : <code>Ctrl+T</code>). 
    To ensure that the exerciseis created correctly, make sure the CSV file is saved properly.</p>

<p>When you create an exercise, you can choose the number of questions it will contain, as well as which rows of the CSV will be used when creating it.</p>

<p>The exercise is presented as a table, with only one cell per row shown. 
    The goal of the exercise is therefore to fill in the remaining cells in each row. You can choose which column to display (the first, the last, or a random one).</p>

<h4 id = "Mode-exercice">2.4 Mode exercice</h4>
<p>The goal of this exercise is to fill in all the empty cells in the table, using the shown cell as a guide.</p>
<p>When you complete an exercise, the toolbar offers two options : <code>Check</code> and <code>Reload</code>.
    <ul>
        <li>The first option allows you to check the anwsers entered in the table. 
        The score is then calculated as follows: 1 point for each correct cell, 
        out of the total number of expected answers.</li>
        <li>The second option allows you to recreate a new exercise from the same file (shortcut: <code>Ctrl+R</code>).
        When you reload an exercise, you can change the exercise's settings (questions number and used rows).</li>
    </ul>
</p>
<p>During the check, the app compares the answers using the default case-insensitive and space-tolerant settings 
    (this option can be changed in the settings; see the next section). Correct answers are highlighted in green, and incorrect ones in red. 
    A GIF may appear depending on the score obtained (this option is also optional).</p>

<p>You can export exercises to PDF, cf <a href="#Edition-de-fichier-CSV">2.2 Editing CSV files</a></p>

<h4 id="Parametres">2.5 Configure the application</h4>

<p>To change the application settings,
    go to the <code>Settings</code> menu and select the <code>Settings...</code> option (shortcut <code>Ctrl+,</code>).
    This will open a window where you can change the settings. The following settings can be modified:
    <ul>
        <li>Application language</li>
        <li>Application style</li>
        <li>When checking answers: </li>
            <ul>
                <li>Case sensitivity</li>
                <li>Space tolerance</li>
            </ul>
        <li>Whether or not to display a GIF when showing the score</li>
        <li>The column displayed during the exercise</li>
        <li>The separator used when reading and writing CSV files</li>
    </ul>
</p>
<p>All of these settings can be reset using the 
    <code>Reset Settings</code> option in the <code>Settings</code> menu.</p>
<p>All settings are saved in the <code>config.toml</code> file, located in the <code>.revitab</code> folder.</p>

<h4 id="Licences-et-user-guide">2.6 Licenses et User guide</h4>

<p>To view the licenses for the application and the icons used, go to the <code>Help</code> menu, then select <code>About</code>.
   To open the README file, select <code>User Guide</code> from the same menu (shortcut <code>F1</code>). 
   The documentation and information are therefore integrated directly into the application.</p>

<h3 id="Liste-raccourcis">Appendix: List of Shortcuts</h3>

<ul>
    <li><code>Ctrl+O</code> : Open</li>
    <li><code>Ctrl+N</code> : New</li>
    <li><code>Ctrl+S</code> : Save</li>
    <li><code>Ctrl+P</code> : Export</li>
    <li><code>Ctrl+T</code> : Create exercise</li>
    <li><code>Ctrl+R</code> : Reload the exercise</li>
    <li><code>Ctrl+Shift+S</code> : Insert an ß</li>
    <li><code>Alt+F4</code> : Exit</li>
    <li><code>Ctrl+,</code> : Settings</li>
    <li><code>F1</code>     : User guide</li>
</ul>

<h3>Enjoy using it !</h3>
</body>
</html>
