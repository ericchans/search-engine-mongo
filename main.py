from search import search
import json

def main():
    query = input("Search: ")
    results = search(query)
    
    print("Top Websites")
    if len(results) != 0:
        print("Showing the first 20 results of " + str(len(results)) + ":")

        for url in range(len(results)):
            print(str(url+1)+'. ' +results[url])

            if url == 19:
                break
    else:
        print("No results found")
        
    print()
    print()
    
if __name__ == '__main__':
    while True:
        main()
        
