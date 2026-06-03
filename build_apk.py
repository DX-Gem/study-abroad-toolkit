import zipfile, os, sys, tempfile

out = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\18391\Desktop\claude code\study-abroad-toolkit\frontend\toolkit.apk'
srcdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(tempfile.gettempdir(), 'apk_rebuild')

if os.path.exists(out):
    os.remove(out)
    print('Removed old APK')

count = 0
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(srcdir):
        for f in files:
            if '.DS_Store' in f:
                continue
            path = os.path.join(root, f)
            arcname = os.path.relpath(path, srcdir).replace('\\', '/')
            zf.write(path, arcname)
            count += 1

print(f'Done: {count} files, {os.path.getsize(out):,} bytes')
