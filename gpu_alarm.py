import os
import time
import argparse

#mail package
import smtplib
from email.mime.text import MIMEText

INIT_INFO = 9
JUMP = 4
NUM_INFO = 1
MEM_INFO = 8
GMAIL_INDEX = 587

parser = argparse.ArgumentParser(description='arguments yaml load')
parser.add_argument("--SLEEP_TIME",
                    type=int,
                    help="sleep tiem in loop(sec)",
                    default=5)

parser.add_argument("--LIMIT_MEM",
                    type=int,
                    help="decide about memory useage(MiB)",
                    default=1000)

parser.add_argument("--file_name",
                    type=str,
                    help="save text file",
                    default="gpu_use.txt")

parser.add_argument("--trcat_gpu_num",
                    nargs="+",
                    type=int,
                    help="tracking gpu number[list]",
                    default=[0])

parser.add_argument("--alias",
                    type=str,
                    help="send email subject",
                    default='my-local')     
parser.add_argument("--email",
                    type=str,
                    help="send email subject",
                    default='my-local') 
parser.add_argument("--app_pw",
                    type=str,
                    help="send email subject") 

args = parser.parse_args()

if __name__ == "__main__":
    send_email = False
    pre_list = args.trcat_gpu_num
    while True:
        os.system(f'nvidia-smi > {args.file_name}')
        with open(args.file_name, 'r') as f:
            ll = f.readlines()
            seq_list = []
            for i in range(INIT_INFO, len(ll), JUMP):
                # print(f'{i}/{len(ll)}')
                c = ll[i].split()
                if len(c) == 1:
                    break

                gpu_num = ll[i-1].split()[NUM_INFO]

                if int(gpu_num) in args.trcat_gpu_num and int(c[MEM_INFO][:-3]) > args.LIMIT_MEM:
                    seq_list.append(int(gpu_num))

            if  len(pre_list) > len(seq_list):
                pre_set = set(pre_list)
                cur_set = set(seq_list)

                smtp = smtplib.SMTP('smtp.gmail.com', GMAIL_INDEX)
                smtp.starttls()  # TLS 사용시 필요
                smtp.login(args.email, args.app_pw)
                
                content = pre_set.difference(cur_set)
                msg = MIMEText(f'{content} empty')
                msg['Subject'] = f'[{args.alias} GPU 사용량]'
                msg['To'] = args.email
                smtp.sendmail(args.email, args.email, msg.as_string())
                smtp.quit()
            print(f'{pre_list}/{seq_list}')
            pre_list = seq_list
        time.sleep(args.SLEEP_TIME)