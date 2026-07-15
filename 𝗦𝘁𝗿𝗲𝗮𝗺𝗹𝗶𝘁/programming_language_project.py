import streamlit as st

st.title("Favorite Programming Language Downloader")

st.write("Download any programming language directly.")

languages = [
    "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript", "Go", "Rust", "Kotlin",
    "Swift", "PHP", "Ruby", "R", "MATLAB", "Scala", "Dart", "Julia", "Perl", "Lua",
    "Haskell", "Elixir", "Erlang", "F#", "OCaml", "Visual Basic .NET", "Objective-C", "Groovy", "Fortran", "COBOL",
    "Ada", "Lisp", "Scheme", "Prolog", "Bash", "PowerShell", "SQL", "SAS", "ABAP", "Assembly",
    "VHDL", "Verilog", "Nim", "Zig", "Crystal", "Solidity", "Apex", "Tcl", "LabVIEW", "Scratch"
]

links = {
    "Python": "https://www.python.org/downloads/",
    "Java": "https://www.oracle.com/java/technologies/downloads/",
    "C": "https://gcc.gnu.org/",
    "C++": "https://gcc.gnu.org/",
    "C#": "https://dotnet.microsoft.com/download",
    "JavaScript": "https://nodejs.org/",
    "TypeScript": "https://www.typescriptlang.org/download/",
    "Go": "https://go.dev/dl/",
    "Rust": "https://www.rust-lang.org/tools/install",
    "Kotlin": "https://kotlinlang.org/"
}

lang = st.selectbox("Choose your programming language:", languages)

st.write("You selected:", lang)

st.success(f"Download {lang} from here:")

if lang in links:
    st.link_button("Official Website", links[lang])
else:
    st.info("Official download link not added yet.")