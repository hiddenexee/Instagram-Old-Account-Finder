from os import system
from uuid import uuid4
from secrets import token_hex
from requests import post
from threading import Lock
import concurrent.futures

lock = Lock()

def __uuid() -> str:
    return str(uuid4())

def check_user(user: str) -> None:
    try:
        device_id = __uuid()

        data = {
            'params': '{"client_input_params":{"is_whatsapp_installed":0,"fetched_email_token_list":{},"was_headers_prefill_available":0,"android_build_type":"release","accounts_list":[],"fetched_email_list":[],"sso_accounts_auth_data":[],"was_headers_prefill_used":0,"ig_android_qe_device_id":"' + device_id + '","headers_infra_flow_id":"","ig_oauth_token":[],"search_query":"' + user + '","encrypted_msisdn":"","sfdid":"","lois_settings":{"lara_override":"","lois_token":""},"text_input_id":"1k5mm5:40"},"server_params":{"is_platform_login":0,"is_from_logged_out":0,"context_data":"","qe_device_id":"' + device_id + '","family_device_id":"' + __uuid() + '","is_from_logged_in_switcher":0,"event_request_id":"' + str(uuid4()) + '","offline_experiment_group":"caa_launch_ig4a_combined_60_percent","INTERNAL_INFRA_THEME":"default","INTERNAL__latency_qpl_instance_id":9432108500068,"device_id":"' + f"android-{token_hex(16)}" + '","INTERNAL__latency_qpl_marker_id":36707139}}',
            'bk_client_context': '{"bloks_version":"8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb","styles_id":"instagram"}',
            'bloks_versioning_id': '8ca96ca267e30c02cf90888d91eeff09627f0e3fd2bd9df472278c9a6c022cbb',
        }

        response = post(
            'https://i.instagram.com/api/v1/bloks/apps/com.bloks.www.caa.ar.search.async/',
            headers={
                'X-Ig-App-Locale': 'tr_TR',
                'X-Ig-Device-Locale': 'tr_TR',
                'X-Ig-Mapped-Locale': 'tr_TR',
                'User-Agent': 'Instagram 275.0.0.27.98 Android (25/7.1.2; 320dpi; 720x1280; samsung; SM-A908N; aosp; android_x86; tr_TR; 458229257)'
            },
            data=data,
            proxies=proxies,
            timeout=10
        ).text

        if 'Tekrar denemeden' in response:
            print("[-] IP blocked")
            file_name = "ip_blocked"
        elif 'USER_NOT_FOUND' in response:
            print("[-] Kullanıcı bulunamadı =>", user)
            file_name = "not_user"
        elif 'e-posta gönderdik' in response:
            print("[+] Mail gönderildi =>", user)
            file_name = "send_email"
        elif 'auth_method_password_back_button_clicked_client' in response:
            print(f"[-] Hesap mevcut, mail gönderilmedi =>", user)
            file_name = "not_send_email"
        else:
            print("[-] Bilinmedik bir sorun oluştu")
            file_name = "none"
    except:
        print("[-] Network error")
        file_name = "network_error"

    with lock:
        open(f"output/{file_name}.txt", "a+").write(user + "\n")

if __name__ == '__main__':
    system("cls")
    system("title Instagram Old Account Finder ^| @hiddenexe")

    users = open("data/users.txt", "r", encoding="utf-8").read().splitlines() # email or username list
    proxy = "user:pass@ip:port" # If you do not use a proxy, you will be banned after 100 scans.

    proxies = {'http': proxy, 'https': proxy}
    #proxies = None
    thread_count = 20

    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        future_to_account = {executor.submit(check_user, user.split(':')[0]): user for user in users}
        for future in concurrent.futures.as_completed(future_to_account):
            try:
                future.result()
            except:
                pass




