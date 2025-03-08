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
# Define Topic Pools Based on Engagement Scores
# ---------------------------
def define_topic_pools(topic_engagement_dict, low_threshold=0.3, high_threshold=0.7):
    """
    Partition topics into low, mid, and high engagement pools based on their scores.
    
    Parameters:
        topic_engagement_dict: Dictionary mapping topic to its engagement score.
        low_threshold: Topics with scores below this value are in the low pool.
        high_threshold: Topics with scores >= this value are in the high pool.
    
    Returns:
        Dictionary with keys "low", "mid", "high" mapping to lists of topics.
    """
    low_pool = [topic for topic, score in topic_engagement_dict.items() if score < low_threshold]
    mid_pool = [topic for topic, score in topic_engagement_dict.items() if low_threshold <= score < high_threshold]
    high_pool = [topic for topic, score in topic_engagement_dict.items() if score >= high_threshold]
    return {"low": low_pool, "mid": mid_pool, "high": high_pool}


topic_engagement_dict = {
    # Low Engagement (0.3 or below)
    "Healthcare": 0.25,
    "Childcare": 0.30,
    "Gun Control": 0.20,
    "Housing Costs": 0.28,
    "Food Insecurity": 0.22,
    "Immigration": 0.27,
    "Reproductive Rights": 0.26,
    "Corrupt Forces": 0.29,
    "Tax Policy": 0.30,
    "LGBTQ Rights": 0.23,

    # Medium Engagement (Between 0.31 - 0.69)
    "Education": 0.35,
    "Environment": 0.55,
    "Misinformation": 0.50,
    "Social Security": 0.40,
    "Rural Broadband": 0.60,
    "Dark Money": 0.45,
    "Public Safety": 0.65,
    "Minimum Wage": 0.48,
    "Criminal Justice": 0.58,
    "Union Rights": 0.42,

    # High Engagement (0.7 or above)
    "Economy": 0.75,
    "Voting Rights": 0.80,
    "Climate Change": 0.75,
    "Women Rights": 0.95,
    "Job Growth": 0.70,
    "Mental Health": 0.72,
    "Drug Pricing": 0.74,
    "Elder Care": 0.85,
    "Infrastructure": 0.78,
    "Civic Engagement": 0.90
}

topics_pool = define_topic_pools(topic_engagement_dict, low_threshold=0.3, high_threshold=0.7)

# ---------------------------
# Helper Functions for Simulation
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

def update_topic_prior(prior, topics, email_outcomes):
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
    return updated

def compute_policy(prior, gamma=1.0):
    topics = list(prior.keys())
    prior_probs = np.array([prior[t] for t in topics])
    logits = np.log(prior_probs + 1e-8) * gamma
    exp_logits = np.exp(logits)
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

# ---------------------------
# Modified Simulation Function Using Engagement-Dependent Topic Pools
# ---------------------------
def simulation_cond(N, T, tau0, lambda_, k_min, k_max, version, topics_pool, thresholds=(0.3, 0.7)):
    """
    Run the simulation over N users and T time periods with engagement-dependent topic pools.
    
    Parameters:
        N: Number of users.
        T: Total simulation time steps.
        tau0: Baseline email interval.
        lambda_: Scheduling sensitivity parameter.
        k_min, k_max: Minimum and maximum topics per email.
        version: 1 for deterministic, 2 for stochastic response function.
        topics_pool: Dictionary mapping engagement level ("low", "mid", "high") to list of topics.
        thresholds: Tuple to categorize engagement scores (e.g., (0.3, 0.7)).
    """
    recorded_data = []
    
    states = {}
    rhos = {}
    next_send = {}
    histories = {}
    user_betas = {}
    
    priors = {}
    for n in range(N):
        priors[n] = {}
        for level, topic_list in topics_pool.items():
            priors[n][level] = {topic: 1 / len(topic_list) for topic in topic_list}
    
    # For unknown response function, set logit parameters per engagement category.
    if version == 2:
        np.random.seed(42)
        topic_logit_params = {}
        for level, topic_list in topics_pool.items():
            topic_logit_params[level] = {topic: np.random.randn(4) for topic in topic_list}
    
    # Assign beta distribution parameters to each user.
    num_beta = len(distributions)
    for n in range(N):
        states[n] = initialize_user_state()
        _, _, alpha, beta_param = distributions[n % num_beta]
        user_betas[n] = (alpha, beta_param)
        rhos[n] = sample_engagement_level(user_betas[n])
        next_send[n] = 0
        histories[n] = []
    
    p_low = [0.45, 0.20, 0.15, 0.20]
    p_high = [0.30, 0.20, 0.25, 0.25]
    
    # Simulation loop over time steps.
    for t in range(T + 1):
        for n in range(N):
            if t >= next_send[n]:
                # 1) Get current engagement level
                engage_score = states[n]["engagement"]
                
                # 2) Determine engagement category.
                if engage_score < thresholds[0]:
                    cat = "low"
                elif engage_score < thresholds[1]:
                    cat = "mid"
                else:
                    cat = "high"
                
                # 3) Use the current engagement category's prior and topic pool.
                current_prior = priors[n][cat]
                topic_dist = compute_policy(current_prior, gamma=1.0)
                
                # 4) Decide how many topics to send and sample from the current pool.
                k = determine_number_of_topics(k_min, k_max)
                topics = sample_topics(topic_dist, k)
                
                # 5) Determine response probabilities and sample outcomes.
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
                
                # 6) Update user information.
                histories[n] = update_history(histories[n], topics, email_outcomes)
                states[n] = update_user_state(states[n], topics, email_outcomes)
                updated_engage_score = compute_engage_score(histories[n])
                rhos[n] = update_engagement_level(rhos[n], states[n], topics, email_outcomes)
                
                # 7) Update the prior for the current engagement category.
                priors[n][cat] = update_topic_prior(current_prior, topics, email_outcomes)
                
                # 8) Schedule next send based on updated engagement.
                delta_t = tau0 * np.exp(-lambda_ * updated_engage_score)
                next_send[n] = t + delta_t
                
                # 9) Record simulation data.
                record = {
                    "user": n,
                    "time": t,
                    "beta_params": user_betas[n],
                    "rho": rhos[n],
                    "engage_score": updated_engage_score,
                    "state": states[n].copy(),
                    "engagement_category": cat,
                    "prior": current_prior,
                    "topic_dist": topic_dist,
                    "topics": topics,
                    "response_probs": response_probs_record,
                    "outcomes": email_outcomes,
                    "next_send": next_send[n],
                }
                recorded_data.append(record)
    return recorded_data