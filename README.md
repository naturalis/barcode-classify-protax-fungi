# barcode-classify-protax-fungi
Profiling PROTAX-fungi for quick and coarse classification of ITS metabarcoding reads.

This is a repository for the implementation of the PROTAX-fungi classifier for the single-level classification of metabarcoded environmental samples using PROTAX-fungi.

Sources:
The data used in this project is from the following github page:
* https://github.com/luukromeijn/MDDB-phylogeny/tree/main, specifically:
  * MDDB-phylogeny/results/thesis results/l0.2_s3_4_1500_o2.0_a1/supertree/backbone.fasta
  * MDDB-phylogeny/results/thesis results/l0.2_s3_4_1500_o2.0_a1/chunks/unaligned
Specifically, the first recommended tree was used. location:

All scripts directly related to running PROTAX-fungi are taken from the following github pages:
* https://github.com/psomervuo/protaxfungi
* https://github.com/TU-NHM/protax_fungi_plutof_pub/tree/master

Other (thirdparty) applications needed for running this repository are Krona (KronaTools-2.6.1) and USEARCH (usearch10.0.240_i86linux32).
* KRONA:
https://www.drive5.com/usearch/download.html
* USEARCH:
https://github.com/marbl/Krona/wiki

# How to install

1. ** Step 1 **
If you are running this on a Windows PC, make sure to install a WSL.

I did so following the instructions on the [WSL documentation](https://learn.microsoft.com/en-us/windows/wsl/install)

2. ** Step 2 ** Run protax_fungi_plutof.def. This does the following things:
   * Installs PROTAX itself via https://raw.githubusercontent.com/psomervuo/protaxfungi/master/protaxfungi.tgz
   * Installs VSEARCH via https://github.com/torognes/vsearch/releases/download/v2.15.1/vsearch-2.15.1-linux-x86_64.tar.gz
   * Installs Krona via https://github.com/marbl/Krona/releases/download/v2.7.1/KronaTools-2.7.1.tar
   

3. ** Step 3 ** Add the following Git submodule to your project folder. This can be done using the following code:
```
#!/bin/bash
git submodule add https://github.com/luukromeijn/MDDB-phylogeny MDDB-phylogeny
```
---------------------------------------

NOTE: It is possible for Krona to install as empty files instead of Perl scripts.
If this happens, follow these steps:
1) Manually download Krona from https://github.com/marbl/Krona/wiki.

2) Open the tar file using:
```
#!/bin/bash
cd thirdparty
tar xvf KronaTools-2.6.1.tar
cd KronaTools-2.6.1
perl install.pl --prefix ../krona
```

3) Copy the perl scripts to the krona/bin file in your project. 
    
Next, for the run_protax.sh script to work, these Perl scripts need to change names.
Specifically, it needs to say 'kt' in front of the name. This is achieved using the following script(s).
    
4) Route to your krona/bin directory containing the Perl script
    
5) Use one of the following scripts to change filenames:
* Windows (PS)

```
# powershell
Get-ChildItem | ForEach-Object {
    $newName = $_.Name
    $firstLetter = $newName[0].ToString().ToUpper()
    $newName = 'kt' + $firstLetter + $newName.Substring(1)
    Rename-Item -Path $_.FullName -NewName $newName
}
```

* OS/Linux/bash:
```
#!/bin/bash
for file in *; do
    newName="kt${file^}"  # Capitalize first letter
    mv "$file" "$newName"
done
```

6) Manually change ktKronaTools.pm back to its original name (KronaTools.pm). 


You are now ready to use Krona. 


## How to run
1. ** Step 1 ** Data Preparation: Make sure all data is prepared in the data file. 
2. ** Step 2 ** Open your WSL and route to the workflow directory
3. ** Step 3 ** Create a venv that contains the packages listed in requirements.txt. Activate this environment
4. ** Step 4 ** Run the following commmand:
```
#!/bash/bin
snakemake -c 1 run_protax
```


### Repository layout

    barcode-classify-protax-fungi
    ├── MDDB-phylogeny
    │   ├── results
    │   └── src
    └── workflow
        ├── data
        │    ├── backbone.fasta
        │    └── sintaxits1_All_Data.fasta
        ├── db_files
        │    ├── file 1
        │    └── file 2
        ├── model
        ├── protaxscripts
        ├── scripts
        ├── thirdparty
        └── userdir
