from NailSalon.settings import BASE_DIR

def open_time_job():
    import helper.techs_queue as techs_queue
    from datetime import date, datetime
    
    current_date = date(2022, 12, 11)
    print(f"[{current_date}]")
    techs_queue.build_fresh_wait_queue(current_date, f"{BASE_DIR}/helper/temp1")
    print(f"- Built fresh queue at [{datetime.now().time()}]\n")