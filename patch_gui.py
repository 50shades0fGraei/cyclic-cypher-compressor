import re
with open('windows_vault_gui.py', 'r') as f:
    content = f.read()

# Replace filedialog.askopenfilename with filedialog.askopenfilenames
new_content = content.replace('target_file = filedialog.askopenfilename(title="Select File to Crunch", filetypes=filetypes)',
                              'target_files = filedialog.askopenfilenames(title="Select File(s) to Crunch (Up to 6 for Bundles)", filetypes=filetypes)')

new_content = new_content.replace('''        if not target_file: return
        
        output_file = target_file + ".cdv6"
        self.run_thread(lujan_core.double_crunch_compress, target_file, output_file)''', '''        if not target_files: return
        
        target_files = self.tk.splitlist(target_files) if isinstance(target_files, str) else target_files
        
        if len(target_files) == 1:
            target_file = target_files[0]
            output_file = target_file + ".cdv6"
            self.run_thread(lujan_core.double_crunch_compress, target_file, output_file)
        else:
            # Bundle them
            import tarfile, os
            import time
            bundle_name = f"bundle_{int(time.time())}.tar"
            bundle_path = os.path.join(os.path.dirname(target_files[0]), bundle_name)
            
            print(f"Bundling {len(target_files)} assets for Double Crunch...")
            with tarfile.open(bundle_path, "w") as tar:
                for tf in target_files:
                    tar.add(tf, arcname=os.path.basename(tf))
            
            output_file = bundle_path + ".cdv6"
            self.run_thread(lujan_core.double_crunch_compress, bundle_path, output_file)
''')

with open('windows_vault_gui.py', 'w') as f:
    f.write(new_content)
print("GUI patched")
