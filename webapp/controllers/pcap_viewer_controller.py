import pandas as pd

def get_table_segment(pcap_filepath, current_page, total_pages, packets_per_page):
    first_row_index = ((current_page - 1) * 25) + 1

    frame = pd.read_csv(pcap_filepath, sep=',', skiprows=range(1, first_row_index), nrows=packets_per_page)
    
    start_page = 1 if current_page <= 4 else  (current_page - 5) // 3 * 3 + 4
    
    start_page = max(min(start_page, total_pages - 5), 1)
    end_page = min(start_page + 5, total_pages)

    packets_to_display = [frame.columns.tolist()]
    packets_to_display += frame.values.tolist()

    return packets_to_display, start_page, end_page