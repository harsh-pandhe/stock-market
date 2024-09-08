mod matching_engine;
use matching_engine::engine::{TradingPair, MatchingEngine};
use matching_engine::orderbook::{BidOrAsk, Order, Orderbook};

fn main() {
    let buy_order_from_mihir = Order::new(BidOrAsk::Bid, 5.5);
    let buy_order_from_harsh = Order::new(BidOrAsk::Bid, 2.45);

    let mut orderbook = Orderbook::new();
    orderbook.add_order(4.4, buy_order_from_mihir);
    orderbook.add_order(4.4, buy_order_from_harsh);

    let sell_order_from_mihir = Order::new(BidOrAsk::Ask, 5.5);
    let sell_order_from_harsh = Order::new(BidOrAsk::Ask, 2.45);

    orderbook.add_order(4.4, sell_order_from_mihir);
    orderbook.add_order(4.4, sell_order_from_harsh);

    // println!("{:?}", orderbook);

    let mut engine = MatchingEngine::new();
    let pair = TradingPair::new("BTC".to_string(), "USDT".to_string());
    engine.add_new_market(pair.clone());

    let buy_order = Order::new(BidOrAsk::Bid, 6.5);
    let  eth_pair = TradingPair::new("ETH".to_string(), "USDT".to_string());
    engine.place_limit_order(pair, 10.000, buy_order).unwrap();
    // engine.place_limit_order(eth_pair, 10.000, buy_order).unwrap();

}
