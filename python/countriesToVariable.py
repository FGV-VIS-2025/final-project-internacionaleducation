import csv

# Caminhos dos arquivos
education_path = 'python/education.csv'
countries_path = 'python/countries.csv'

# 1. Coletar países do education.csv
education_countries = set()

with open(education_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        education_countries.add(row['Country'].strip())

# 2. Gerar lista JS apenas para países usados
entries = []

with open(countries_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['Name'].strip()
        code = row['Code'].strip().lower()

        if name in education_countries:
            entries.append(f'  {{ name: "{name}", code: "{code}" }}')

# 3. Monta o JS final
js_output = "const countriesISO = [\n" + ",\n".join(sorted(entries)) + "\n];"

# 4. Exibe no terminal
print(js_output)

# 5. (Opcional) Salva em arquivo
with open('countriesISO.js', 'w', encoding='utf-8') as f:
    f.write(js_output)
