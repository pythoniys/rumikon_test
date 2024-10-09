import re
from collections import Counter

def clean_html(html_content):
    clean_text = re.sub(r'<.*?>', '', html_content)
    return clean_text

def extract_words(text):
    words = re.findall(r'\b\w{3,}\b', text.lower())  
    return words

def main():
    file_path = input("Введите путь к HTML файлу: ")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        clean_text = clean_html(html_content)

        words = extract_words(clean_text)

        word_counts = Counter(words)

        top_10_words = word_counts.most_common(10)

        print("Топ 10 слов:")
        for word, count in top_10_words:
            print(f"{word}: {count}")

    except FileNotFoundError:
        print("Файл не найден.")

if __name__ == "__main__":
    main()
