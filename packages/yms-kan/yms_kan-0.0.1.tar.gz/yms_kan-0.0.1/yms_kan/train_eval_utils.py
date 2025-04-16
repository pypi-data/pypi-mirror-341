import math
import os
import sys
from enum import Enum, auto

import numpy as np
import torch
from matplotlib import pyplot as plt
from torch.optim.lr_scheduler import ReduceLROnPlateau
from tqdm import tqdm

from yms_kan import LBFGS


class TaskType(Enum):
    classification = auto()
    zlm = auto()


def train_val(model, dataset: dict, batch_size, batch_size_test, opt="LBFGS", epochs=100, lamb=0.,
              lamb_l1=1., label=None, lamb_entropy=2., lamb_coef=0.,
              lamb_coefdiff=0., update_grid=True, grid_update_num=10, loss_fn=None, lr=1., start_grid_update_step=-1,
              stop_grid_update_step=100,
              save_fig=False, in_vars=None, out_vars=None, beta=3, save_fig_freq=1, img_folder='./video',
              singularity_avoiding=False, y_th=1000., reg_metric='edge_forward_spline_n'):
    # result_info = ['epoch','train_losses', 'val_losses', 'regularize', 'accuracies',
    #                'precisions', 'recalls', 'f1-scores']
    # initialize_results_file(results_file, result_info)
    all_predictions = []
    all_labels = []
    if lamb > 0. and not model.save_act:
        print('setting lamb=0. If you want to set lamb > 0, set model.save_act=True')

    old_save_act, old_symbolic_enabled = model.disable_symbolic_in_fit(lamb)
    if label is not None:
        label = label.to(model.device)

    if loss_fn is None:
        loss_fn = lambda x, y: torch.mean((x - y) ** 2)
    else:
        loss_fn = loss_fn

    grid_update_freq = int(stop_grid_update_step / grid_update_num)

    if opt == "Adam":
        optimizer = torch.optim.Adam(model.get_params(), lr=lr)
    elif opt == "LBFGS":
        optimizer = LBFGS(model.get_params(), lr=lr, history_size=10, line_search_fn="strong_wolfe",
                          tolerance_grad=1e-32, tolerance_change=1e-32, tolerance_ys=1e-32)
    else:
        optimizer = torch.optim.SGD(model.get_params(), lr=lr)

    lr_scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=5, min_lr=1e-9)

    results = {'train_losses': [], 'val_losses': [], 'regularize': [], 'accuracies': [],
               'precisions': [], 'recalls': [], 'f1-scores': []}

    steps = math.ceil(dataset['train_input'].shape[0] / batch_size)

    train_loss = torch.zeros(1).to(model.device)
    reg_ = torch.zeros(1).to(model.device)

    def closure():
        nonlocal train_loss, reg_
        optimizer.zero_grad()
        pred = model.forward(batch_train_input, singularity_avoiding=singularity_avoiding, y_th=y_th)
        loss = loss_fn(pred, batch_train_label)
        if model.save_act:
            if reg_metric == 'edge_backward':
                model.attribute()
            if reg_metric == 'node_backward':
                model.node_attribute()
            reg_ = model.get_reg(reg_metric, lamb_l1, lamb_entropy, lamb_coef, lamb_coefdiff)
        else:
            reg_ = torch.tensor(0.)
        objective = loss + lamb * reg_
        train_loss = (train_loss * batch_num + objective.detach()) / (batch_num + 1)
        objective.backward()
        return objective

    if save_fig:
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)

    for epoch in range(epochs):

        if epoch == epochs - 1 and old_save_act:
            model.save_act = True

        if save_fig and epoch % save_fig_freq == 0:
            save_act = model.save_act
            model.save_act = True

        train_indices = np.arange(dataset['train_input'].shape[0])
        np.random.shuffle(train_indices)
        train_pbar = tqdm(range(steps), desc=f'Epoch {epoch + 1}/{epochs} Training', file=sys.stdout)
        for batch_num in train_pbar:
            step = epoch * steps + batch_num + 1
            i = batch_num * batch_size
            batch_train_id = train_indices[i:i + batch_size]
            batch_train_input = dataset['train_input'][batch_train_id].to(model.device)
            batch_train_label = dataset['train_label'][batch_train_id].to(model.device)

            if step % grid_update_freq == 0 and step < stop_grid_update_step and update_grid and step >= start_grid_update_step:
                model.update_grid(batch_train_input)

            if opt == "LBFGS":
                optimizer.step(closure)

            else:
                optimizer.zero_grad()
                pred = model.forward(batch_train_input, singularity_avoiding=singularity_avoiding,
                                     y_th=y_th)
                loss = loss_fn(pred, batch_train_label)
                if model.save_act:
                    if reg_metric == 'edge_backward':
                        model.attribute()
                    if reg_metric == 'node_backward':
                        model.node_attribute()
                    reg_ = model.get_reg(reg_metric, lamb_l1, lamb_entropy, lamb_coef, lamb_coefdiff)
                else:
                    reg_ = torch.tensor(0.)
                loss = loss + lamb * reg_
                train_loss = (train_loss * batch_num + loss.detach()) / (batch_num + 1)
                loss.backward()
                optimizer.step()
            train_pbar.set_postfix(loss=train_loss.item())

        val_loss = torch.zeros(1).to(model.device)
        with torch.no_grad():
            test_indices = np.arange(dataset['test_input'].shape[0])
            np.random.shuffle(test_indices)
            test_steps = math.ceil(dataset['test_input'].shape[0] / batch_size_test)
            test_pbar = tqdm(range(test_steps), desc=f'Epoch {epoch + 1}/{epochs} Validation', file=sys.stdout)
            for batch_num in test_pbar:
                i = batch_num * batch_size_test
                batch_test_id = test_indices[i:i + batch_size_test]
                batch_test_input = dataset['test_input'][batch_test_id].to(model.device)
                batch_test_label = dataset['test_label'][batch_test_id].to(model.device)

                outputs = model.forward(batch_test_input, singularity_avoiding=singularity_avoiding,
                                        y_th=y_th)

                loss = loss_fn(outputs, batch_test_label)

                val_loss = (val_loss * batch_num + loss.detach()) / (batch_num + 1)
                test_pbar.set_postfix(loss=loss.item(), val_loss=val_loss.item())
                if label is not None:
                    diffs = torch.abs(outputs - label)
                    closest_indices = torch.argmin(diffs, dim=1)
                    closest_values = label[closest_indices]
                    all_predictions.extend(closest_values.detach().cpu().numpy())
                    all_labels.extend(batch_test_label.detach().cpu().numpy())

            lr_scheduler.step(val_loss)

        results['train_losses'].append(train_loss.cpu().item())
        results['val_losses'].append(val_loss.cpu().item())
        results['regularize'].append(reg_.cpu().item())

        if save_fig and epoch % save_fig_freq == 0:
            model.plot(folder=img_folder, in_vars=in_vars, out_vars=out_vars, title="Step {}".format(epoch),
                       beta=beta)
            plt.savefig(img_folder + '/' + str(epoch) + '.jpg', bbox_inches='tight', dpi=100)
            plt.close()
            model.save_act = save_act

    # append_to_results_file(results_file, results, result_info)
    model.log_history('fit')
    model.symbolic_enabled = old_symbolic_enabled
    return results


if __name__ == '__main__':
    print(TaskType.zlm.value)
