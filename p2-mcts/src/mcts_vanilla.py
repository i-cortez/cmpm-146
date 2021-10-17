
from mcts_node import MCTSNode
from random import choice
from math import inf, sqrt, log

num_nodes = 100
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.
    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.
    Returns:        A node from which the next stage of the search can proceed.
    """
    # Set to the initial state
    current_node = node
    # To hold the highest value of UCB1 found thus far
    # max_ucb1 = 0
    depth = 0
    T_state = state
    best_ucb1 = 0
    min_ucb1 = inf
    while not board.is_ended(state) and current_node is not None:
        #print("depth=",depth)
        # Loop while there are nodes to visit
        if current_node.child_nodes == {}:
            # We have found a leaf node
            #print("empty child node")
            return current_node
        else:
            # A leaf node has not been found yet
            depth += 1
            original_current_node = current_node
            num_children_tested = 0
            for action in original_current_node.child_nodes:
                #print(key_value)
                child = original_current_node.child_nodes.get(action)
                # if board.legal_actions(state)
                num_children_tested += 1
                if child.visits == 0:
                    return child
                elif identity == board.current_player(T_state):
                    # The current player wishes to maximize ucb1
                    v = child.wins / child.visits
                    radical = sqrt(log(child.parent.visits) / child.visits)
                    ucb1 = v + (explore_faction * radical)
                    if ucb1 > best_ucb1:
                        best_ucb1 = ucb1
                        current_node = child
                else:
                    # The curent player wishes to minimize ucb1 for opponent
                    v = 1 - (child.wins / child.visits)
                    radical = sqrt(log(child.parent.visits) / child.visits)
                    ucb1 = v + (explore_faction * radical)
                    if ucb1 < best_ucb1:
                        best_ucb1 = ucb1
                        current_node = child
            T_state = board.next_state(T_state, current_node.parent_action)
            if original_current_node == current_node:
                print("no child found after ", num_children_tested, " tests")
                return current_node
    # No leaf node was found so return None
    return None

    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.
    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.
    Returns:    The added child node.
    """

    new_action = choice(node.untried_actions)
    # new_action = node.untried_actions[0]
    new_state = board.next_state(state, new_action)
    new_node = MCTSNode(node, new_action, board.legal_actions(new_state))
    node.child_nodes.update({new_action: new_node})
    return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.
    Args:
        board:  The game setup.
        state:  The state of the game.
    """

    while not board.is_ended(state):
        rollout_move = choice(board.legal_actions(state))
        state = board.next_state(state, rollout_move)
    return state

def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.
    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.
    """

    if node.parent is None:
        # Base case: has reached the root node
        return
    node.wins += won
    node.visits += 1
    backpropagate(node.parent, won)

def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.
    Args:
        board:  The game setup.
        state:  The state of the game.
    Returns:    The action to be taken.
    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        #print(step)
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        #print("traverse")
        leaf_node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        #print("traverse done")
        #print("add")
        if leaf_node.visits != 0:
            while leaf_node.untried_actions != []:
                new_node = expand_leaf(leaf_node, board, sampled_game)
                leaf_node.untried_actions.pop(0)
            leaf_node = new_node
        #print("add done")
        #print("rollout")
        won = rollout(board, sampled_game)
        #print("roll done")
        """
        result = board.win_values(sampled_game)
        if result is not None:
            # Try to normalize it up?  Not so sure about this code anyhow.
            player1 = result[1]
            player2 = result[2]
        else:
            player1 = player2 = 0
        if player1 == player2:
            player1 = player2 = 0
        if identity_of_bot == board.current_player(sampled_game):
            if identity_of_bot == 1:
                won = player1
            else:
                won = player2
        else:
            if identity_of_bot == 1:
                won = player2
            else:
                won = player1
        #print("backp")
        """
        backpropagate(leaf_node, won[identity_of_bot])
        #print("back done")

    #print(node.tree_to_string(5, 1))

    moves = board.legal_actions(state)
    #print(moves)
    highest_win = 0
    most_repeated = 0
    best_move = moves[0]
    most_used_move = moves[0]
    #print(node.child_nodes.keys())

    for move in moves:
        #print(node.parent_action)
        #print(move)
        x = node.child_nodes.get(move)
        if x is None:
            continue
        #print(x.wins)
        if x.visits != 0:
            win_rate = x.wins / x.visits
        else:
            return move
        if win_rate > highest_win:
            highest_win = win_rate
            best_move = move
        if x.visits > most_repeated:
            most_repeated = x.visits
            most_used_move = move
    #print("turn taken")
    if highest_win < 0:
        return most_used_move

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return best_move

