from metaml.parameter_space.node import CategoricalNode, FloatNode, IntegerNode
from metaml.parameter_space.set import CategoricalSet, FloatSet, IntegerSet


booster = CategoricalNode(
    name="booster",
    label="Booster",
    description="Specifies the core boosting algorithm, determining the type of base learners in the ensemble model.",
    domain=CategoricalSet(categories={"dart", "gbtree"}),
    enabled=False,
    default_value="gbtree",
    constraint=False,
    constraintInformation=None,
)
colsample_bylevel = FloatNode(
    name="colsample_bylevel",
    label="Column subsample ratio by level",
    description="Fraction of features randomly sampled for each level in the decision tree during construction.",
    domain=FloatSet.closed(0.5, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
colsample_bynode = FloatNode(
    name="colsample_bynode",
    label="Column subsample ratio by node",
    description="Fraction of features randomly sampled for each new node in the decision tree during construction.",
    domain=FloatSet.closed(0.5, 1.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
colsample_bytree = FloatNode(
    name="colsample_bytree",
    label="Column subsample ratio by tree",
    description="Fraction of features randomly sampled for each tree during model construction.",
    domain=FloatSet.closed(0.5, 1.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
gamma = FloatNode(
    name="gamma",
    label="Gamma",
    description="Minimum reduction in loss function required to create a new tree split, controlling model complexity and preventing overfitting.",
    domain=FloatSet.closed(0.0, 10.0),
    enabled=True,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
learning_rate = FloatNode(
    name="learning_rate",
    label="Learning rate",
    description="Step size shrinkage used in updates to prevent overfitting by shrinking feature weights, making the boosting process more conservative.",
    domain=FloatSet.closed(0.005, 0.4),
    enabled=True,
    default_value=0.3,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_delta_step = FloatNode(
    name="max_delta_step",
    label="Maximum delta step",
    description="Maximum allowed change for each leaf output in the tree, mitigating the influence of outliers or skewed data by limiting weight updates.",
    domain=FloatSet.closed(0.0, 10.0),
    enabled=False,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
max_depth = IntegerNode(
    name="max_depth",
    label="Maximum depth",
    description="Maximum depth of the tree. Nodes are expanded until all leaves are pure or contain less than min_samples_split samples.",
    domain=IntegerSet.closedopen(3, 11),
    enabled=True,
    default_value=9,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
min_child_weight = FloatNode(
    name="min_child_weight",
    label="Minimum child weight",
    description="Minimum number of training examples required in each tree node to allow further splitting.",
    domain=FloatSet.closed(0.0, 10.0),
    enabled=False,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
n_estimators = IntegerNode(
    name="n_estimators",
    label="Number of estimators",
    description="Number of trees built during the training process.",
    domain=IntegerSet.closedopen(10, 501),
    enabled=True,
    default_value=100,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
num_parallel_tree = IntegerNode(
    name="num_parallel_tree",
    label="Number of parallel trees",
    description="Number of parallel trees constructed during each iteration, supporting boosted random forests.",
    domain=IntegerSet.closedopen(1, 11),
    enabled=False,
    default_value=1,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
reg_alpha = FloatNode(
    name="reg_alpha",
    label="Regularization alpha",
    description="Strength of L1 regularization term, penalizing absolute values of leaf node weights, promoting sparsity and reducing overfitting risk.",
    domain=FloatSet.closed(0.0, 0.1),
    enabled=True,
    default_value=0.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
reg_lambda = FloatNode(
    name="reg_lambda",
    label="Regularization lambda",
    description="Strength of L2 regularization term, penalizing squared values of leaf node weights, encouraging smaller weights and reducing overfitting.",
    domain=FloatSet.closed(0.5, 2.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
subsample = FloatNode(
    name="subsample",
    label="Subsample",
    description="Fraction of training examples randomly sampled without replacement for each tree, reducing overfitting and improving generalization.",
    domain=FloatSet.closed(0.65, 1.0),
    enabled=True,
    default_value=1.0,
    constraint=False,
    constraintInformation=None,
    distribution="uniform",
)
tree_method = CategoricalNode(
    name="tree_method",
    label="Tree method",
    description="Algorithm used to construct decision trees during the training process.",
    domain=CategoricalSet(categories={"exact", "gpu_hist", "hist", "approx"}),
    enabled=False,
    default_value="hist",
    constraint=False,
    constraintInformation=None,
)

parameter_nodes = [
    booster,
    colsample_bylevel,
    colsample_bynode,
    colsample_bytree,
    gamma,
    learning_rate,
    max_delta_step,
    max_depth,
    min_child_weight,
    n_estimators,
    num_parallel_tree,
    reg_alpha,
    reg_lambda,
    subsample,
    tree_method,
]
