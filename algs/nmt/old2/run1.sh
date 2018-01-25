python nmt.py \
    --src=vi --tgt=en \
    --vocab_prefix=/home/burak/Downloads/nmt_data/vocab  \
    --train_prefix=/home/burak/Downloads/nmt_data/train \
    --dev_prefix=/home/burak/Downloads/nmt_data/tst2012  \
    --test_prefix=/home/burak/Downloads/nmt_data/tst2013 \
    --out_dir=/home/burak/Downloads/nmt_model \
    --num_train_steps=12000 \
    --steps_per_stats=100 \
    --num_layers=2 \
    --num_units=128 \
    --dropout=0.2 \
    --metrics=bleu
