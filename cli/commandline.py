import datetime as dt
import argparse

def valid_date(s):
    try: 
        return dt.datetime.strptime(s, "%d/%m/%Y")
    except ValueError:
        try: 
            return dt.datetime.strptime(s,"%d/%m/%Y %H:%M:%S")
        except ValueError:
            msg = "\nInput date: {0!r} is not a valid date format. \
            \nPlease use dd/mm/yyyy or 'dd/mm/yyyy hh:mm:ss'.".format(s)
            raise argparse.ArgumentTypeError(msg)

def main():
    parser = argparse.ArgumentParser(description='CLI for securely downloading data from the FTP server.')
    parser.add_argument('--startdate','-s',type=valid_date)
    parser.add_argument('--enddate','-e',type=valid_date)
    parser.add_argument('--encrypt','-E',type=str)


    args = parser.parse_args()
    print("The start date selected is: "+str(args.startdate)) 
    print("The end date selected is: "+str(args.enddate))


if __name__ == '__main__':
    main()
