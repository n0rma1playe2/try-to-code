# import requests
# username = input("请输入你需要获取的Github用户所有关注者的登录名")
# URL = f'https://api.github.com/users/{username}/followers'
# current_page=1
# params = {'page': current_page, 'per_page': 100}
# session = requests.Session(URL)
# a = session.get(URL,params=params)
# print(a)
import requests 
def get_github_followers(username:str)-> list[str]: 
    URL = f"https://api.github.com/users/{username}/followers"
    session = requests.session()
    all_followers = []
    current_page = 1
    print(f"现在正在抓取{username}的粉丝列表")
    
    while True:
        params ={
            'per_page':100,
            'page' : current_page
        }

        try:
            response = session.get(URL,params=params)
            if response.status_code == 403:
                print("已触发github的api速率限制")
                print("匿名用户每小时只能请求六十次，稍后再试")
                break
            if response.status_code != 200:
                print(f"请求失败，状态码为:{response.status_code},请查询此状态码")
            data = response.json()

            if len(data) == 0:
                print("所有页面都抓取完毕")
                break
            
            for user in data:
                all_followers.append(user['login'])

            print(f"已获取第{current_page}页，本页{len(data)}人")

            current_page += 1

        except Exception as e :
            print(f"发生错误:{e}")
            break
    return all_followers

if __name__ == "__main__":
    target_user = input("请输入你需要查询的用户")

    followers_list = get_github_followers(target_user)
    print("-" * 30)
    print(f"抓取完成！")
    print(f"用户[{target_user}]共有{len(followers_list)}个粉丝")

    print(f"前十个粉丝是:{followers_list[:10]}")