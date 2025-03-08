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
    """
    Standard softmax function over a 1D array of logits z.
    """
    e_x = np.exp(z - np.max(z))
    return e_x / e_x.sum()

def initialize_user_state():
    """
    Initialize a user state with demographic and engagement info.
    """
    gender = np.random.choice(["male", "female"])
    location = np.random.choice(["urban", "suburban", "rural"])
    return {"gender": gender, "location": location, "engagement": 0.0}

def sample_engagement_level(user_beta):
    """
    Sample an initial engagement level rho from the user's beta distribution (alpha, beta_param).
    """
    alpha, beta_param = user_beta
    return np.random.beta(alpha, beta_param)

def determine_number_of_topics(k_min, k_max):
    """
    Draw k number of topics uniformly between k_min and k_max (inclusive).
    """
    return np.random.randint(k_min, k_max + 1)

def compute_engage_score(history, m=5):
    """
    Compute the engagement score (ES) as the average cost over the past m outcomes.
    Cost structure for the four outcomes:
    1 -> 1, 2 -> 2, 3 -> 3, 4 -> 5
    """
    cost_dict = {1: 1, 2: 2, 3: 3, 4: 5}
    if len(history) == 0:
        return 0.0
    recent = history[-m:]
    score = np.mean([cost_dict.get(y, 0) for y in recent])
    return score

def sample_topics(topic_dist, k):
    """
    Sample k topics without replacement from the topic set, according to topic_dist.
    
    topic_dist: a dictionary {topic: probability}
    """
    topics = list(topic_dist.keys())
    probs = np.array([topic_dist[t] for t in topics])
    selected = np.random.choice(topics, size=k, replace=False, p=probs)
    return list(selected)

def sample_outcome(prob_vector):
    """
    Given a probability vector for the 4 outcomes, sample an outcome in {1, 2, 3, 4}.
    """
    outcomes = np.array([1, 2, 3, 4])
    return np.random.choice(outcomes, p=prob_vector)

def update_history(history, topics, email_outcomes):
    """
    Update the user's history with the outcomes from the current email.
    """
    history.extend(email_outcomes)
    return history

def update_user_state(state, topics, email_outcomes):
    """
    Update the user state based on the outcomes.
    Here we just update an 'engagement' field as a simple function of average outcome.
    """
    if email_outcomes:
        avg_outcome = np.mean(email_outcomes)
        state["engagement"] = 0.5 * state["engagement"] + 0.5 * (avg_outcome / 5)
    return state

def update_engagement_level(rho, state, topics, email_outcomes):
    """
    Update the engagement level (rho) based on the new outcomes.
    We shift rho slightly toward the normalized average outcome.
    """
    if email_outcomes:
        avg_outcome = np.mean(email_outcomes)
        new_rho = rho + 0.1 * ((avg_outcome / 5) - rho)
        return np.clip(new_rho, 0, 1)
    else:
        return rho

def update_topic_prior(prior, topics, email_outcomes, smoothing=0.1):
    """
    Update the topic prior via a Bayesian-like update.
    Parameters:
        prior: current topic prior dictionary
        topics: list of topics updated in the current email send
        email_outcomes: outcomes from the current email send
        smoothing: mixing weight for the uniform prior (between 0 and 1)
    Returns:
        A smoothed topic prior.
    """
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

def compute_policy(prior, gamma=1.0):
    """
    Compute the updated topic distribution using a softmax transformation.
    π(x | ES_t) ∝ π₀(x) exp{γ ⋅ φ(x, ES_t)}.
    Here we use the prior values and a simple softmax.
    """
    topics = list(prior.keys())
    prior_probs = np.array([prior[t] for t in topics])
    logits = np.log(prior_probs + 1e-8) * gamma
    exp_logits = np.exp(logits)
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
    topic_logit_params: {topic: [logit1, logit2, logit3, logit4]}
    
    We return a dictionary: {topic: [p1, p2, p3, p4]} where p_i are softmax probabilities for outcome i.
    """
    response_dict = {}
    
    for topic in topics:
        logits = np.array(topic_logit_params[topic])
        probs = softmax(logits)  # shape (4,)
        response_dict[topic] = probs
    
    return response_dict

# ---------------------------
# Simulation Function
# ---------------------------
def simulation(N, T, tau0, lambda_, k_min, k_max, version, topics_list):
    """
    Run the simulation over N users and T time periods.
    
    Parameters:
        N: Number of users (e.g., 2000)
        T: Total simulation time steps (e.g., hours for 30 days)
        tau0: Baseline email interval (e.g., 24 hours)
        lambda_: Scheduling sensitivity parameter
        k_min, k_max: Minimum and maximum topics per email
        version: 1 for deterministic response function, 2 for stochastic
        topics_list: List of topics to use in the simulation
    """
    recorded_data = []
    pi0 = {topic: 1 / len(topics_list) for topic in topics_list}

    # For unknown response function, set logit parameters per topic.
    if version == 2:
        np.random.seed(42)
        topic_logit_params = {topic: np.random.randn(4) for topic in topics_list}
                    
    states = {}
    rhos = {}
    next_send = {}
    histories = {}
    priors = {}
    user_betas = {}
    
    # Assign beta distribution parameters to each user (cycled from the closed distributions)
    num_beta = len(distributions)
    for n in range(N):
        states[n] = initialize_user_state()
        _, _, alpha, beta_param = distributions[n % num_beta]
        user_betas[n] = (alpha, beta_param)
        rhos[n] = sample_engagement_level(user_betas[n])
        next_send[n] = 0 
        histories[n] = []  
        priors[n] = pi0.copy()
    
    # Fixed response probability vectors for deterministic response for 4 outcomes:
    p_low = [0.45, 0.20, 0.15, 0.20]   # Outcome (Y) 1: open, 2: click, 3: volunteer, 4: donate
    p_high = [0.30, 0.20, 0.25, 0.25]
    
    for t in range(T + 1):
        for n in range(N):
            if t >= next_send[n]:
                # 1) Compute current engagement score from history
                engage_score = compute_engage_score(histories[n])
                topic_prior = priors[n].copy()
                
                # 2) Compute current topic distribution from prior
                topic_dist = compute_policy(priors[n], gamma=1.0)
                
                # 3) Decide how many topics to send
                k = determine_number_of_topics(k_min, k_max)
                topics = sample_topics(topic_dist, k)

                # 4) Determine response probabilities and sample outcomes
                email_outcomes = []
                response_probs_record = {}  # record response probabilities for each topic

                if version == 1:
                    blend_probs = compute_response_probs_deterministic(rhos[n], p_low, p_high)
                    for topic in topics:
                        y = sample_outcome(blend_probs)
                        email_outcomes.append(y)
                        response_probs_record[topic] = blend_probs.tolist()
                elif version == 2:
                    response_probs_dict = compute_response_probs_stochastic(
                        states[n], topics, topic_logit_params
                    )
                    for topic in topics:
                        probs_for_topic = response_probs_dict[topic]
                        y = sample_outcome(probs_for_topic)
                        email_outcomes.append(y)
                        response_probs_record[topic] = probs_for_topic.tolist()
                else:
                    email_outcomes = []

                # 5) Update agent information
                histories[n] = update_history(histories[n], topics, email_outcomes)
                states[n] = update_user_state(states[n], topics, email_outcomes)
                updated_engage_score = compute_engage_score(histories[n])
                rhos[n] = update_engagement_level(rhos[n], states[n], topics, email_outcomes)
                priors[n] = update_topic_prior(priors[n], topics, email_outcomes)

                # 6) Email Scheduling
                delta_t = tau0 * np.exp(-lambda_ * updated_engage_score)
                next_send[n] = t + delta_t

                # 7) Record simulation data
                record = {
                    "user": n,
                    "time": t,
                    "beta_params": user_betas[n],
                    "rho": rhos[n],
                    "engage_score": updated_engage_score,
                    "state": states[n].copy(),
                    "prior": topic_prior,
                    "topic_dist": topic_dist,
                    "topics": topics,
                    "response_probs": response_probs_record,
                    "outcomes": email_outcomes,
                    "next_send": next_send[n],
                }
                recorded_data.append(record)
    return recorded_data