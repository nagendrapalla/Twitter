import preprocessor as p  # used for cleaning text


def mention_hydrate(entity_list):
    x = 0  # list index
    i = 1  # list length
    container = []
    entity_length = len(entity_list)
    while i <= entity_length:
        temp_list = entity_list[x]
        j = temp_list.get("username")
        container.append(j)
        i = i + 1
        x = x + 1
    return container


def hashtag_hydrate(entity_list):
    x = 0  # list index
    i = 1  # list length
    container = []
    entity_length = len(entity_list)
    while i <= entity_length:
        temp_list = entity_list[x]
        j = temp_list.get("tag")
        container.append(j)
        i = i + 1
        x = x + 1
    return container


def url_hydrate(entity_list):
    x = 0  # list index
    i = 1  # list length
    container = []
    entity_length = len(entity_list)
    while i <= entity_length:
        temp_list = entity_list[x]
        j = temp_list.get("expanded_url")
        container.append(j)
        i = i + 1
        x = x + 1
    return container


def annotations_hydrate(entity_list):
    x = 0  # list index
    i = 1  # list length
    container = []
    entity_length = len(entity_list)
    while i <= entity_length:
        temp_list = entity_list[x]
        t = temp_list.get("type")
        container.append(t)
        n = temp_list.get("normalized_text")
        container.append(n)
        i = i + 1
        x = x + 1
    return container


def remove_whitespace(text):
    return " ".join(text.split())


def clean_tweets(tweet_text):
    p.set_options(p.OPT.URL, p.OPT.MENTION)
    clean_tweet_text = p.clean(tweet_text)
    clean_tweet_text = remove_whitespace(clean_tweet_text)
    clean_tweet_text = clean_tweet_text.replace('&amp', "")

    return clean_tweet_text


def makeitastring(wannabestring):
    convertedstring = ','.join(map(str, wannabestring))
    return convertedstring


def hydrate_public_metrics(tweet_dict):
    if 'public_metrics' in tweet_dict:
        public_metrics_dict = (tweet_dict['public_metrics'])
        tweet_retweet_count = public_metrics_dict.get('retweet_count')
        tweet_like_count = public_metrics_dict.get('like_count')
        tweet_quote_count = public_metrics_dict.get('quote_count')
        tweet_reply_count = public_metrics_dict.get('reply_count')
    return tweet_retweet_count, tweet_like_count, tweet_quote_count, tweet_reply_count


def hydrate_referenced_tweets(referenced_tweets):
    if referenced_tweets:
        string = makeitastring(referenced_tweets)
        string = string.replace("<ReferencedTweet ", "")
        string = string.replace("id=", "").replace("type=", "")
        string = string.replace("[", "").replace("]", "")
        referenced_tweets_list = string.split(" ")
        ref_type = referenced_tweets_list[1]
        ref_id = referenced_tweets_list[0]
    else:
        ref_type = "original"
        ref_id = None
    return ref_type, ref_id


def hydrate_entities(tweet_entities):
    empty = "None"
    ent_dict = []
    ent_dict = tweet_entities
    if 'mentions' in ent_dict:
        t_mentions = ent_dict.get('mentions')
        tweet_mentions = mention_hydrate(t_mentions)  #
        tweet_mentions = makeitastring(tweet_mentions)

    else:
        tweet_mentions = empty

    if 'hashtags' in ent_dict is not None:  # is not None needed????
        t_hashtags = ent_dict.get('hashtags')
        tweet_hashtags = hashtag_hydrate(t_hashtags)  #
        tweet_hashtags = makeitastring(tweet_hashtags)

    else:
        tweet_hashtags = empty

    if 'annotations' in ent_dict:
        t_annotations = ent_dict.get('annotations')
        tweet_annotations = annotations_hydrate(t_annotations)  #
        tweet_annotations = makeitastring(tweet_annotations)

    else:
        tweet_annotations = empty

    if 'urls' in ent_dict:
        t_urls = ent_dict.get('urls')
        tweet_urls = url_hydrate(t_urls)  #
        tweet_urls = makeitastring(tweet_urls)
    else:
        tweet_urls = empty

    return tweet_mentions, tweet_hashtags, tweet_annotations, tweet_urls


def remove_duplicates_in_list(test_list):
    test_list = list(set(test_list))
    return (test_list)


def hydrate_context_annotations(tweet_data):
    empty = "None"
    tweet_domains = []
    tweet_entities = []
    tweet_entities_no_dup = []
    tweet_domains_no_dup = []
    if 'context_annotations' in tweet_data:
        for annotation in tweet_data['context_annotations']:
            d = annotation["domain"]["name"]
            e = annotation["entity"]["name"]
            tweet_domains.append(d)
            tweet_entities.append(e)
            tweet_domains_no_dup = remove_duplicates_in_list(tweet_domains)
            tweet_domains_no_dup = remove_duplicates_in_list(tweet_entities)

    else:
        tweet_entities_no_dup = empty
        tweet_domains_no_dup = empty

    tweet_entities_no_dup = makeitastring(tweet_entities)
    tweet_domains_no_dup = makeitastring(tweet_domains)
    return tweet_entities_no_dup, tweet_domains_no_dup


def influence_score(tweet_user_verified, tweet_user_tweet_count, tweet_user_followers_count, tweet_user_listed_count,
                    tweet_user_like_count):
    score = 0
    if tweet_user_verified:
        score = score + 4000
    if tweet_user_tweet_count > 0:
        score = score + (tweet_user_tweet_count * .05)
    if tweet_user_followers_count > 0:
        score = score + (tweet_user_followers_count * .2)
    if tweet_user_listed_count > 0:
        score = score + (tweet_user_listed_count * 200)
    if tweet_user_like_count > 0:
        temp_user_like_score = (tweet_user_like_count * .05)
        if temp_user_like_score > 10000:
            score = score + 10000
        else:
            score = score + temp_user_like_score
    temp_score = (score / 10000)
    influence = round(temp_score, 2)
    return (influence)
