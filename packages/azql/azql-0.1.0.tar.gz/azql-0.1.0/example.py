import azql

fp = "data/sample"
script = azql.convert(fp, output_dir="tmp", schema="stage")
print(script)
