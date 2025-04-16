
import datetime
import time
import quote_module.quote_module as qm
from collections import defaultdict

dict_serial_number = defaultdict(int)


def callback_pcap_read(quote: qm.QuoteS):
    pass
    if quote.pause != 0:
        print(quote)
        print(f'{quote.code_str} {quote.timestamp_str} close: {quote.close_price}, bool close:{quote.bool_close}, volume: {quote.close_volume}, '
              f'volume acc: {quote.volume_acc}, ask price: {quote.ask_price}, ask volume: {quote.ask_volume}, bid price: {quote.bid_price}, bid volume: {quote.bid_volume}, '
              f'bool continue: {quote.bool_continue}, bool bid price: {quote.bool_bid_price}, bool ask price: {quote.bool_ask_price}, bool odd: {quote.bool_odd}, '
              f'num ask: {quote.number_best_ask}, num bid: {quote.number_best_bid}, tick type: {quote.tick_type}, bool simtrade: {quote.bool_simtrade}, Pause: {quote.pause}, '
              f'now second: {quote.double_now_seconds}, msg type: {quote.message_type}, serial: {quote.serial_number}\n\n')

    last_serial_number = dict_serial_number[quote.message_type]
    if quote.serial_number != last_serial_number + 1:
        print(f'Error: {quote.message_type} {quote.serial_number} {last_serial_number}')
    dict_serial_number[quote.message_type] = quote.serial_number


if False:
    qm.INTERFACE_IP_TSE = '10.175.2.17' 
    qm.INTERFACE_IP_OTC = '10.175.1.17' 
    qm.INTERFACE_IP_FUT = '10.71.17.74'
    qm.set_mc_live_pcap_callback(callback_pcap_read)
    qm.start_mc_live_pcap_read()


if True:
    qm.set_offline_pcap_callback(callback_pcap_read)
    qm.start_offline_pcap_read('/home/william/tcpdump/TSEOTC-2025-01-02.pcap')


while True:
    ret = qm.check_offline_pcap_read_ended()
    if ret != 0:
        break
    print(f'{datetime.datetime.now()} {ret}')
    time.sleep(1)
