import os, json
import torch
from tqdm import tqdm

from modules.dataset_init import prepare_dataset
from modules.infer_lib import grab_corpus_feature, eval_epoch 

from utils.basic_utils import AverageMeter, get_logger
from utils.setup import set_seed, get_args
from utils.run_utils import prepare_optimizer, prepare_model, logger_ndcg_iou

def main():
    opt = get_args()
    logger = get_logger(opt.results_path, opt.exp_id)
    set_seed(opt.seed)
    logger.info("Arguments:\n%s", json.dumps(vars(opt), indent=4))
    opt.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"device: {opt.device}")
    
    
    
    train_loader, corpus_loader, corpus_video_list, val_loader, test_loader, val_gt, test_gt = prepare_dataset(opt)

    model = prepare_model(opt, logger)
    optimizer = prepare_optimizer(model, opt, len(train_loader) * opt.n_epoch)
    
    eval_step = len(train_loader) // opt.eval_num_per_epoch
    best_val_ndcg = 0
    for epoch_i in range(0, opt.n_epoch):
        logger.info(f"TRAIN EPOCH: {epoch_i}|{opt.n_epoch}")
        model.train()
        if opt.hard_negative_start_epoch != -1 and epoch_i >= opt.hard_negative_start_epoch:
            model.set_hard_negative(True, opt.hard_pool_size)

        model.train()
        for step, batch_input in tqdm(enumerate(train_loader), desc="Training", total=len(train_loader)):
            step += 1
            batch_input = {k: v.to(opt.device) for k, v in batch_input.items()}
            loss = model(**batch_input)
            optimizer.zero_grad()
            loss.backward()
            # nn.utils.clip_grad_norm_(model.parameters())
            optimizer.step()
            
            if step % opt.log_step == 0:
                logger.info(f"EPOCH {epoch_i}/{opt.n_epoch} | STEP: {step}|{len(train_loader)} | Loss: {loss.item():.6f}")
                
            if step % eval_step == 0 or step == len(train_loader):
                corpus_feature = grab_corpus_feature(model, corpus_loader, opt.device)
                val_ndcg_iou = eval_epoch(model, corpus_feature, val_loader, val_gt, opt, corpus_video_list)
                test_ndcg_iou = eval_epoch(model, corpus_feature, test_loader, test_gt, opt, corpus_video_list)

                logger_ndcg_iou(val_ndcg_iou, logger, "VAL")
                logger_ndcg_iou(test_ndcg_iou, logger, "TEST")

                if val_ndcg_iou[20][0.5] > best_val_ndcg:
                    best_val_ndcg = val_ndcg_iou[20][0.5]
                    logger_ndcg_iou(val_ndcg_iou, logger, "BEST VAL")
                    logger_ndcg_iou(test_ndcg_iou, logger, "BEST TEST")
                    
                    checkpoint = {"model": model.state_dict(), "model_cfg": model.config, "epoch": epoch_i}

                    bestmodel_path = os.path.join(opt.results_path, "best_model.pt")
                    torch.save(checkpoint, bestmodel_path)
                    logger.info(f"Save checkpoint at {bestmodel_path}")
                    logger.info("")

if __name__ == '__main__':
    main()
