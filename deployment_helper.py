"""
Helper script to prepare the Game of Life for web deployment using Pygbag.
This allows the game to run on any device with a web browser, including iPhones.
"""

import os
import shutil
import subprocess

# Create the web build directory
os.makedirs("web_build", exist_ok=True)

# Copy the main game file to the web build directory
shutil.copy("life.py", "web_build/main.py")

# Create a simple HTML template file
with open("web_build/index.html", "w") as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Game of Life - iPhone 15 Pro</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #000;
            touch-action: manipulation;
            overflow: hidden;
        }
        #canvas {
            display: block;
            margin: 0 auto;
            touch-action: manipulation;
        }
    </style>
</head>
<body>
    <!-- Game canvas will be inserted here by Pygbag -->
    <script type="module">
        import { loadPyodide } from 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.mjs';
        
        async function main() {
            const pyodide = await loadPyodide();
            await pyodide.loadPackagesFromImports('main.py');
            await pyodide.runPythonAsync(`
                import asyncio
                from pyodide.http import pyfetch
                response = await pyfetch("main.py")
                with open("main.py", "wb") as f:
                    f.write(await response.bytes())
                
                # Load and run the Python code
                import main
                asyncio.ensure_future(main.main())
            `);
        }
        main();
    </script>
</body>
</html>
    """)

print("Web deployment files created in the 'web_build' directory")
print("To build and run the web version: pygbag --port 8000 web_build")