import pytest

import torch
from evolutionary_policy_optimization import (
    LatentGenePool,
    Actor,
    Critic
)

@pytest.mark.parametrize('num_latent_sets', (1, 4))
def test_readme(
    num_latent_sets
):

    latent_pool = LatentGenePool(
        num_latents = 128,
        dim_latent = 32,
        dim_state = 512,
        num_latent_sets = num_latent_sets
    )

    state = torch.randn(1, 512)

    actor = Actor(dim_state = 512, dim_hiddens = (256, 128), num_actions = 4, dim_latent = 32)
    critic = Critic(dim_state = 512, dim_hiddens = (256, 128, 64), dim_latent = 32)

    latent = latent_pool(latent_id = 2, state = state)

    actions = actor(state, latent)
    value = critic(state, latent)

    # interact with environment and receive rewards, termination etc

    # derive a fitness score for each gene / latent

    fitness = torch.randn(128)

    latent_pool.genetic_algorithm_step(fitness) # update once


def test_create_agent():
    from evolutionary_policy_optimization import create_agent

    agent = create_agent(
        dim_state = 512,
        num_latents = 128,
        dim_latent = 32,
        actor_num_actions = 5,
        actor_dim_hiddens = (256, 128),
        critic_dim_hiddens = (256, 128, 64)
    )

    state = torch.randn(1, 512)

    actions = agent.get_actor_actions(state, latent_id = 3)
    value = agent.get_critic_values(state, latent_id = 3)

    # interact with environment and receive rewards, termination etc

    # derive a fitness score for each gene / latent

    fitness = torch.randn(128)

    agent.update_latent_gene_pool_(fitness) # update once
