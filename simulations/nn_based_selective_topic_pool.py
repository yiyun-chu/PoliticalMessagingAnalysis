import numpy as np
from scipy.stats import beta, wasserstein_distance
import torch
import torch.nn as nn
import torch.optim as optim
from scipy.special import logsumexp

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------------------
# Generate Closed Beta Distributions
# ---------------------------
def generate_closed_beta_distributions(num_distributions=26, range_start=0, range_end=25):
    distributions = []
    for i in range(num_distributions):
        alpha = 1.6 + (i * 0.2)
        beta_param = max(5.2 - (i * 0.2), 2)
        x = np.linspace(0, 1, 100)
        y = beta.pdf(x, alpha, beta_param)
        x_scaled = x * (range_end - range_start) + range_start
        distributions.append((x_scaled, y, alpha, beta_param))
    return distributions

distributions = generate_closed_beta_distributions()

# ---------------------------
# Helper Functions
# ---------------------------
def softmax(z):
    e_x = np.exp(z - np.max(z))
    return e_x / e_x.sum()

def initialize_user_state():
    gender = np.random.choice(["male", "female"])
    location = np.random.choice(["urban", "suburban", "rural"])
    latent_taste = np.random.randn(3)
    return {"gender": gender, "location": location, "engagement": 0.0, "latent_taste": latent_taste}

def sample_engagement_level(user_beta):
    alpha, beta_param = user_beta
    return np.random.beta(alpha, beta_param)

def determine_number_of_topics(k_min, k_max):
    return np.random.randint(k_min, k_max + 1)

def compute_engage_score(history, m=5):
    cost_dict = {1: 1, 2: 2, 3: 3, 4: 5}
    if len(history) == 0:
        return 0.0
    recent = history[-m:]
    score = np.mean([cost_dict.get(y, 0) for y in recent])
    return score

def sample_topics(topic_dist, k):
    topics = list(topic_dist.keys())
    probs = np.array([topic_dist[t] for t in topics])
    selected = np.random.choice(topics, size=k, replace=False, p=probs)
    return list(selected)

def sample_outcome(prob_vector):
    outcomes = np.array([1, 2, 3, 4])
    return np.random.choice(outcomes, p=prob_vector)

def update_history(history, topics, email_outcomes):
    history.extend(email_outcomes)
    return history

def update_user_state(state, topics, email_outcomes, alpha=0.1):
    if email_outcomes:
        avg_outcome = np.mean(email_outcomes)
        state["engagement"] = (1 - alpha) * state["engagement"] + alpha * (avg_outcome / 5)
    return state

def update_engagement_level(rho, state, topics, email_outcomes):
    if email_outcomes:
        avg_outcome = np.mean(email_outcomes)
        new_rho = rho + 0.1 * ((avg_outcome / 5) - rho)
        return np.clip(new_rho, 0, 1)
    else:
        return rho

def update_topic_prior(prior, topics, email_outcomes, smoothing=0.2):
    updated = prior.copy()
    if email_outcomes:
        good = np.sum(np.array(email_outcomes) >= 3)
        factor = 1 + 0.1 * (good / len(email_outcomes))
    else:
        factor = 1.0
    for t in topics:
        updated[t] *= factor
    total = sum(updated.values())
    for t in updated:
        updated[t] /= total
    uniform_prior = {t: 1/len(prior) for t in prior}
    smoothed = {t: (1 - smoothing) * updated[t] + smoothing * uniform_prior[t] for t in updated}
    total_smoothed = sum(smoothed.values())
    for t in smoothed:
        smoothed[t] /= total_smoothed
    return smoothed

def encode_demographics(state):
    gender = state.get("gender", "male")
    gender_onehot = [1, 0] if gender == "male" else [0, 1]
    
    location = state.get("location", "urban")
    if location == "urban":
        location_onehot = [1, 0, 0]
    elif location == "suburban":
        location_onehot = [0, 1, 0]
    else:
        location_onehot = [0, 0, 1]
    
    return np.array(gender_onehot + location_onehot)

def state_feat(state):
    engagement = np.array([state.get("engagement", 0.0)])
    demographic_features = encode_demographics(state)
    latent_taste = state.get("latent_taste", np.zeros(3))
    return np.concatenate((engagement, demographic_features, latent_taste))

def compute_policy(prior, state, gamma):
    topics = list(prior.keys())
    prior_probs = np.array([prior[t] for t in topics])
    
    features = state_feat(state)
    if np.isscalar(gamma):
        gamma_cat = gamma * np.ones_like(features)
    elif isinstance(gamma, dict):
        cat = state.get("engagement_category", "low")
        gamma_cat = gamma.get(cat, np.ones_like(features))
    else:
        gamma_cat = gamma
        
    gamma_effective = np.dot(gamma_cat, features)
    
    logits = np.log(prior_probs + 1e-8) * gamma_effective
    exp_logits = np.exp(logits - np.max(logits))
    policy = exp_logits / exp_logits.sum()
    
    return dict(zip(topics, policy))

def compute_response_probs_deterministic(rho, p_low, p_high):
    return (1 - rho) * np.array(p_low) + rho * np.array(p_high)

def compute_response_probs_stochastic(state, topics, topic_logit_params):
    response_dict = {}
    for topic in topics:
        logits = np.array(topic_logit_params[topic])
        probs = softmax(logits)
        response_dict[topic] = probs
    return response_dict

def compute_policy_nn(policy_model, prior, state):
    topics = sorted(prior.keys())
    prior_vec = np.array([prior[t] for t in topics], dtype=np.float32)
    engagement = np.array([state.get("engagement", 0.0)], dtype=np.float32)
    demographics = encode_demographics(state).astype(np.float32)
    input_vector = np.concatenate([prior_vec, engagement, demographics])
    
    required_dim = policy_model.fc1.in_features
    if input_vector.shape[0] < required_dim:
        pad_width = required_dim - input_vector.shape[0]
        input_vector = np.concatenate([input_vector, np.zeros(pad_width, dtype=np.float32)])
    elif input_vector.shape[0] > required_dim:
        input_vector = input_vector[:required_dim]
    
    input_tensor = torch.from_numpy(input_vector).float().unsqueeze(0).to(device)
    
    with torch.no_grad():
        policy_probs = policy_model(input_tensor).squeeze(0).cpu().numpy()
    
    policy_probs /= policy_probs.sum()
    return dict(zip(topics, policy_probs))

def email_scheduling_interval(tau0, lambda_, updated_engage_score, min_interval=1):
    return max(min_interval, tau0 * np.exp(-lambda_ * updated_engage_score))

# ---------------------------
# Selective Topic Pools
# ---------------------------
def define_topic_pools_binary(topic_engagement_dict, threshold=0.3):
    low_pool = [topic for topic, score in topic_engagement_dict.items() if score < threshold]
    high_pool = [topic for topic, score in topic_engagement_dict.items() if score >= threshold]
    return {"low": low_pool, "high": high_pool}

topic_engagement_dict = 'YOUR_TOPIC_ENGAGEMENT_DICT'
topics_pool = define_topic_pools_binary(topic_engagement_dict, threshold=0.3)

# ---------------------------
# Simulation Function
# ---------------------------
def simulation_nn_cond_bin(N, T, tau0, lambda_, k_min, k_max, version, topics_pool, 
                            threshold=0.5, gamma=1.0, policy_update_interval=24, buffer=0.05):
    recorded_data = []
    
    priors = {}
    for n in range(N):
        priors[n] = {}
        for level, topic_list in topics_pool.items():
            priors[n][level] = {topic: 1 / len(topic_list) for topic in topic_list}
    
    if version == 2:
        topic_logit_params = {}
        for level, topic_list in topics_pool.items():
            topic_logit_params[level] = {topic: np.random.randn(4) for topic in topic_list}
    
    states, rhos, next_send, histories, user_betas = {}, {}, {}, {}, {}
    num_beta = len(distributions)
    for n in range(N):
        states[n] = initialize_user_state()
        _, _, alpha_val, beta_param = distributions[n % num_beta]
        user_betas[n] = (alpha_val, beta_param)
        rhos[n] = sample_engagement_level(user_betas[n])
        next_send[n] = 0
        histories[n] = []
    
    last_policy = {}
    last_cat = {}
    for n in range(N):
        state_n = states[n]
        engagement = state_n["engagement"]
        cat = "low" if engagement < threshold else "high"
        last_cat[n] = cat
        state_n["engagement_category"] = cat
        current_prior = priors[n][cat]
        last_policy[n] = compute_policy(current_prior, state_n, gamma)
    
    p_low = [0.30, 0.35, 0.15, 0.20]
    p_high = [0.30, 0.20, 0.25, 0.25]
    
    for t in range(T + 1):
        if t % policy_update_interval == 0:
            engagements = np.array([states[n]["engagement"] for n in range(N)])
            median_engagement = np.median(engagements)
            for n in range(N):
                new_cat = "low" if states[n]["engagement"] < median_engagement else "high"
                last_cat[n] = new_cat
                states[n]["engagement_category"] = new_cat
                current_prior = priors[n][new_cat]
                last_policy[n] = compute_policy(current_prior, states[n], gamma)
            cat_counts = {"low": 0, "high": 0}
            for n in range(N):
                cat_counts[states[n]["engagement_category"]] += 1
            print(f"Time {t}: Category counts: {cat_counts}")
        
        for n in range(N):
            if t >= next_send[n]:
                cat = last_cat[n]
                topic_dist = last_policy[n]
                k = determine_number_of_topics(k_min, k_max)
                topics = sample_topics(topic_dist, k)
                
                email_outcomes = []
                response_probs_record = {}
                if version == 1:
                    blend_probs = compute_response_probs_deterministic(rhos[n], p_low, p_high)
                    for topic in topics:
                        y = sample_outcome(blend_probs)
                        email_outcomes.append(y)
                        response_probs_record[topic] = blend_probs.tolist()
                elif version == 2:
                    response_probs_dict = compute_response_probs_stochastic(
                        states[n], topics, topic_logit_params[cat]
                    )
                    for topic in topics:
                        probs_for_topic = response_probs_dict[topic]
                        y = sample_outcome(probs_for_topic)
                        email_outcomes.append(y)
                        response_probs_record[topic] = probs_for_topic.tolist()
                else:
                    email_outcomes = []
                
                histories[n] = update_history(histories[n], topics, email_outcomes)
                states[n] = update_user_state(states[n], topics, email_outcomes, alpha=0.1)
                updated_engage_score = compute_engage_score(histories[n])
                rhos[n] = update_engagement_level(rhos[n], states[n], topics, email_outcomes)
                
                current_prior = priors[n][cat]
                priors[n][cat] = update_topic_prior(current_prior, topics, email_outcomes, smoothing=0.2)
                
                delta_t = email_scheduling_interval(tau0, lambda_, updated_engage_score, min_interval=1)
                next_send[n] = t + delta_t
                
                record = {
                    "user": n,
                    "time": t,
                    "beta_params": user_betas[n],
                    "rho": rhos[n],
                    "engage_score": updated_engage_score,
                    "state": states[n].copy(),
                    "engagement_category": cat,
                    "prior": priors[n][cat],
                    "topic_dist": topic_dist,
                    "topics": topics,
                    "response_probs": response_probs_record,
                    "outcomes": email_outcomes,
                    "next_send": next_send[n],
                }
                recorded_data.append(record)
    return recorded_data