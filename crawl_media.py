import bs4
import os
import requests


def crawl_all_media(path):
    pwd = os.path.abspath(path)
    for file in os.listdir(path):
        file_path = os.path.join(pwd, file)
        print(file_path)
        if os.path.isfile(file_path):
            if file.endswith(".md"):
                if os.path.exists(os.path.join(pwd, file.replace(".md", ".mp3"))):
                    continue
                soup = bs4.BeautifulSoup(open(file_path, encoding='utf-8'), features='html.parser')
                audio_tag = soup.find("audio")
                if audio_tag is not None:
                    audio_url = audio_tag.get("src")
                    # print(f"audio_url:{audio_url}")
                    # print("audio_url:{url}".format(url=audio_url))
                    print("audio_url:%s" % audio_url)
                    rsp = requests.request("GET", audio_url)
                    if rsp.status_code != 200:
                        print(f"response for request url[{audio_url}] is failed, status_code[{rsp.status_code}], reason[{rsp.reason}]")
                    else:
                        with open(os.path.join(pwd, file.replace(".md", ".mp3")), mode="wb") as store_file:
                            write_count = 0
                            try:
                                write_count = store_file.write(rsp.content)
                            except:
                                print("write file[%s] got exception" % store_file.name)
                                continue
                            finally:
                                print("write file[%s] done, write_count[%d]" % (store_file.name, write_count))
                                store_file.flush()
                                store_file.close()
        elif os.path.isdir(file_path):
            if not file.startswith("."):
                crawl_all_media(file_path)
        else:
            print(f"{file} is not file or dir!")


if __name__ == "__main__":
    crawl_all_media(".")
