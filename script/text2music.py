import torch
from samplings import top_p_sampling, temperature_sampling
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import datetime, os, random, glob
from unidecode import unidecode

from tqdm import tqdm

def text2music(num_tunes = 3, max_length = 1024, top_p = 0.9, temperature = 1.0, text = "This is a traditional Irish dance music."):
    """_summary_

    Args:
        num_tunes (int, optional): number of songs. Defaults to 5.
        max_length (int, optional): max lengeth. Defaults to 1024.
        top_p (float, optional): _description_. Defaults to 0.9.
        temperature (float, optional): _description_. Defaults to 1.0.
        text (str, optional): _description_. Defaults to "This is a traditional Irish dance music.".
    """
    
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained('sander-wood/text-to-music')
    model = AutoModelForSeq2SeqLM.from_pretrained('sander-wood/text-to-music')
    model = model.to(device)

    # 曲数
    # num_tunes = 5
    # max_length = 1024
    # max_length = 512
    # top_p = 0.9
    # temperature = 1.0

    # text = "This is a traditional Irish dance music."
    # text = "Please create an exhilarating anime song with a calm atmosphere and a sense of speed, like the opening song of a battle anime. The song begins with a gripping intro that draws you in, followed by a fast-paced drum beat. A calm melody is combined with a powerful chorus, leading to an exhilarating chorus. The song contains hot guitar solos and keyboard performances that make you think of battle scenes, giving you a sense of intensity and power. There is a beautiful melody that envelops the entire song, and at the end of the song, there is a harmony that mixes the chorus and instrumental performances to increase the excitement. This is the song that gives you the courage and determination to go into battle."
    input_ids = tokenizer(text, 
                        return_tensors='pt', 
                        truncation=True, 
                        max_length=max_length)['input_ids'].to(device)

    decoder_start_token_id = model.config.decoder_start_token_id
    eos_token_id = model.config.eos_token_id


    # dt_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    # path = os.getcwd()
    # dir_abc = os.path.join(path, '.\output\ABC')

    # dir_len = len(glob.glob(f'{dir_abc}/*/'))
    # abc_list = os.path.join(dir_abc, f'abc_disc-{dir_len + 1}')

    abc_scores = []
    # 日付のディレクトリの下にabc_discを作ってもいいかもしれない
    for i in tqdm(range(num_tunes)):
        
        # 
        # if not os.path.isdir(abc_list):
        #     os.mkdir(f'{abc_list}')
        
        tune = f"X:{i + 1}\n"
        decoder_input_ids = torch.tensor([[decoder_start_token_id]])    
        
        for t_idx in tqdm(range(max_length)):
            
            rand_seed = random.randint(0, 1000000)
            random.seed(rand_seed)
            
            outputs = model(
                input_ids=input_ids, 
                decoder_input_ids=decoder_input_ids.to(device))
            probs = outputs.logits[0][-1]
            probs = torch.nn.Softmax(dim=-1)(probs).cpu().detach().numpy()
            sampled_id = temperature_sampling(probs=top_p_sampling(probs, 
                                                                top_p=top_p,
                                                                seed=rand_seed,
                                                                return_probs=True),
                                            seed=rand_seed,
                                            temperature=temperature)
            decoder_input_ids = torch.cat((decoder_input_ids, torch.tensor([[sampled_id]])), 1)
            
            if sampled_id!=eos_token_id:
                # sampled_token = tokenizer.decode([sampled_id])
                # tune += sampled_token
                continue
            else:
                tune += tokenizer.decode(decoder_input_ids[0], skip_special_tokens=True)
                tune += '\n'
                print(tune)
                break
        
        abc_scores.append(unidecode(tune))
        # with open(f'{abc_list}\{dt_now}-{i}.abc', 'a') as f:
        #     f.write(f'{unidecode(tune)}')
    
    return abc_scores      
