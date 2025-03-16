import numpy as np
from scipy.stats import beta

# ---------------------------
# Generate Closed Beta Distributions
# ---------------------------
def generate_closed_beta_distributions(num_distributions=26, range_start=0, range_end=25):
    distributions = []
    for i in range(num_distributions):
        alpha = 1.6 + (i * 0.2)
        beta_param = 5.2 - (i * 0.2)
        beta_param = max(beta_param, 2)
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
    return {"gender": gender, "location": location, "engagement": 0.0}

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

def update_user_state(state, topics, email_outcomes):
    if email_outcomes:
        avg_outcome = np.mean(email_outcomes)
        state["engagement"] = 0.5 * state["engagement"] + 0.5 * (avg_outcome / 5)
    return state

def update_engagement_level(rho, state, topics, email_outcomes):
    if email_outcomes:
        avg_outcome = np.mean(email_outcomes)
        new_rho = rho + 0.1 * ((avg_outcome / 5) - rho)
        return np.clip(new_rho, 0, 1)
    else:
        return rho

def update_topic_prior(prior, topics, email_outcomes, smoothing=0.05):
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
    gender_onehot = [1, 0] if gender == "male" else [0, 1]  # [male, female]

    location = state.get("location", "urban")
    location_onehot = [1, 0, 0] if location == "urban" else \
                        [0, 1, 0] if location == "suburban" else \
                        [0, 0, 1]  # [urban, suburban, rural]

    return np.array(gender_onehot + location_onehot)

def compute_policy(prior, state, gamma):
    topics = list(prior.keys())
    prior_probs = np.array([prior[t] for t in topics])
    
    # feature vector
    engagement = np.array([state.get("engagement", 0.0)]) 
    demographic_features = encode_demographics(state)
    feature_vector = np.concatenate((engagement, demographic_features))
    gamma_effective = np.dot(gamma, feature_vector)

    # compute topic selection probabilities
    logits = np.log(prior_probs + 1e-8) * gamma_effective
    exp_logits = np.exp(logits - np.max(logits))
    policy = exp_logits / exp_logits.sum()
    
    return dict(zip(topics, policy))

def compute_response_probs_deterministic(rho, p_low, p_high):
    """
    For the deterministic response function, linearly interpolate between p_low and p_high based on rho.
    """
    return (1 - rho) * np.array(p_low) + rho * np.array(p_high)

def compute_response_probs_stochastic(state, topics, topic_logit_params):
    """
    Use a multinomial logistic (softmax) model for each topic.
    Returns a dictionary: {topic: [p1, p2, p3, p4]} where p_i are softmax probabilities for outcome i.
    """
    response_dict = {}
    for topic in topics:
        logits = np.array(topic_logit_params[topic])
        probs = softmax(logits)
        response_dict[topic] = probs
    return response_dict

# ---------------------------
# Simulation Function
# ---------------------------
def simulation_rule(N, T, tau0, lambda_, k_min, k_max, version, topics_list, policy_update_interval):
    recorded_data = []
    pi0 = {topic: 1 / len(topics_list) for topic in topics_list}

    if version == 2:
        np.random.seed(42)
        topic_logit_params = {topic: np.random.randn(4) for topic in topics_list}

    states = {}
    rhos = {}
    next_send = {}
    histories = {}
    priors = {}
    user_betas = {}
    last_policy = {}
    gamma = np.ones(6)

    num_beta = len(distributions)
    for n in range(N):
        states[n] = initialize_user_state()
        _, _, alpha, beta_param = distributions[n % num_beta]
        user_betas[n] = (alpha, beta_param)
        rhos[n] = sample_engagement_level(user_betas[n])
        next_send[n] = 0
        histories[n] = []
        priors[n] = pi0.copy()
        last_policy[n] = compute_policy(priors[n], states[n], gamma)

    p_low = [0.45, 0.20, 0.15, 0.20]
    p_high = [0.30, 0.20, 0.25, 0.25]

    for t in range(T + 1):
        if t % policy_update_interval == 0:
            for n in range(N):
                priors[n] = update_topic_prior(priors[n], [], [], smoothing=0.1)
                last_policy[n] = compute_policy(priors[n], states[n], gamma)
        
        for n in range(N):
            if t >= next_send[n]:
                topic_dist = last_policy[n] if t % policy_update_interval == 0 else compute_policy(priors[n], states[n], gamma)

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
                    response_probs_dict = compute_response_probs_stochastic(states[n], topics, topic_logit_params)
                    for topic in topics:
                        probs_for_topic = response_probs_dict[topic]
                        y = sample_outcome(probs_for_topic)
                        email_outcomes.append(y)
                        response_probs_record[topic] = probs_for_topic.tolist()
                else:
                    email_outcomes = []

                histories[n] = update_history(histories[n], topics, email_outcomes)
                states[n] = update_user_state(states[n], topics, email_outcomes)
                updated_engage_score = compute_engage_score(histories[n])
                rhos[n] = update_engagement_level(rhos[n], states[n], topics, email_outcomes)
                priors[n] = update_topic_prior(priors[n], topics, email_outcomes)

                delta_t = tau0 * np.exp(-lambda_ * updated_engage_score)
                next_send[n] = t + delta_t

                record = {
                    "user": n,
                    "time": t,
                    "beta_params": user_betas[n],
                    "rho": rhos[n],
                    "engage_score": updated_engage_score,
                    "state": states[n].copy(),
                    "prior": priors[n].copy(),
                    "topic_dist": topic_dist,
                    "topics": topics,
                    "response_probs": response_probs_record,
                    "outcomes": email_outcomes,
                    "next_send": next_send[n],
                }
                recorded_data.append(record)

    return recorded_data