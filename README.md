# Provider Leaderboard

This is the open-sourced backend of [Martian](https://withmartian.com/)'s [provider leaderboard](https://leaderboard.withmartian.com/) which collects metrics daily and track them overtime to evaluate providers' performance on featured models for custom use cases. 

To learn more about how we collect and measure data, view our [Methodology](https://docs.withmartian.com/provider-leaderboard/). Read more about the limitations of this benchmark [here](https://docs.withmartian.com/provider-leaderboard/limitations).


## Getting Started

To run your own backend and replicate how we manage our data collection, create your own `.env` file by following `.env-sample`
```
pip install -r requirements.txt
uvicorn main:app --reload
```

## Disclaimer

We are open sourcing this repo for transparency and reproducibility purposes, but we will not have the bandwidth to respond to every issue quickly. We welcome any feedback from the community, and will respond to all suggestions as soon as possible. For general inquries about [Martian](https://withmartian.com/), feel free to reach out at contact@withmartian.com
