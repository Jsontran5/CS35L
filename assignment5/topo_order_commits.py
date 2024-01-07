#!/usr/local/cs/bin/python3
import os
import sys
import zlib

# I ran: strace -f python3 topo_order_commits.py environ, execl, execle,
# execlp, execv, execve, execvp, fexecve 2>&1 | grep exec, and it equals 0


class CommitNode:
    def __init__(self, commit_hash):
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()


def find_git_directory():
    current_dir = os.getcwd()
    while current_dir != '/':
        git_dir = os.path.join(current_dir, ".git")
        if os.path.exists(git_dir):
            return git_dir
        current_dir = os.path.dirname(current_dir)
    print("Not inside a Git repository", file=sys.stderr)
    sys.exit(1)


def get_local_branches(git_directory):
    branches_dir = os.path.join(git_directory, 'refs', 'heads')
    local_branches = {}
    if os.path.exists(branches_dir):
        for root, _, files in os.walk(branches_dir):
            for file in files:
                branch_name = os.path.relpath(
                    os.path.join(root, file), branches_dir)
                with open(os.path.join(root, file), 'r') as branch_file:
                    commit_hash = branch_file.read().strip()
                    if commit_hash not in local_branches:
                        local_branches[commit_hash] = [branch_name]
                    else:
                        local_branches[commit_hash].append(branch_name)
    return local_branches


def decompress_git_object(git_directory, sha1):
    objects_dir = os.path.join(git_directory, 'objects')
    object_path = os.path.join(objects_dir, sha1[:2], sha1[2:])
    if not os.path.exists(object_path):
        return None
    with open(object_path, 'rb') as obj_file:
        compressed_data = obj_file.read()
    return zlib.decompress(compressed_data).decode('utf-8')


def build_commit_graph(git_directory, local_branches):
    commit_graph = {}
    visited = set()

    for branch_head in local_branches:
        stack = [branch_head]

        while stack:
            commit_hash = stack.pop()
            if commit_hash in visited:
                continue
            visited.add(commit_hash)

            commit_data = decompress_git_object(git_directory, commit_hash)
            if not commit_data:
                continue

            commit_lines = commit_data.split('\n')
            parent_hashes = [line.split(' ')[1]
                             for line in commit_lines
                             if line.startswith('parent')]

            comit_hash = commit_hash
            commit_node = commit_graph.get(comit_hash, CommitNode(commit_hash))

            for parent_hash in parent_hashes:
                if parent_hash not in visited:
                    stack.append(parent_hash)

                parent_node = commit_graph.get(
                    parent_hash, CommitNode(parent_hash))
                commit_node.parents.add(parent_hash)
                parent_node.children.add(commit_hash)
                commit_graph[parent_hash] = parent_node

            commit_graph[commit_hash] = commit_node

    return commit_graph


def topo_sort(commit_graph):
    root_commits = []
    results = []
    parent_count = {}

    for commit_hash, commit_node in commit_graph.items():
        parent_count[commit_hash] = len(commit_node.parents)
        if len(commit_node.parents) == 0:
            root_commits.append(commit_hash)

    while root_commits:
        current_root = root_commits[-1]
        results.append(current_root)
        root_commits.pop()
        c_graph = commit_graph[current_root].children
        commit_graph[current_root].children = sorted(c_graph)
        for child in commit_graph[current_root].children:
            parent_count[child] -= 1
            if parent_count[child] == 0:
                root_commits.append(child)

    return results[::-1]


def print_sorted_order(commit_graph, topo_sorted, local_branches):
    is_path = True
    for i in range(len(topo_sorted)):
        if not is_path:
            is_path = True
            sticky_start = "="
            for child in commit_graph[topo_sorted[i]].children:
                sticky_start += child + " "
            if sticky_start[-1] == " ":
                sticky_start = sticky_start[:-1]
            print(sticky_start)

        if topo_sorted[i] in local_branches:
            local_branches[topo_sorted[i]].sort()
            branch_string = ""
            for branch in local_branches[topo_sorted[i]]:
                branch_string += " " + branch
            print(topo_sorted[i] + branch_string)
        else:
            print(topo_sorted[i])

        sticky_end = ""
        if i == len(topo_sorted) - 1:
            continue
        if topo_sorted[i + 1] not in commit_graph[topo_sorted[i]].parents:
            for parent in commit_graph[topo_sorted[i]].parents:
                sticky_end += parent + " "
            sticky_end = sticky_end[:-1] + "="
            print(sticky_end)
            print()
            is_path = False


def topo_order_commits():
    git_directory = find_git_directory()
    local_branches = get_local_branches(git_directory)
    commit_graph = build_commit_graph(git_directory, local_branches)
    topo_sorted = topo_sort(commit_graph)
    print_sorted_order(commit_graph, topo_sorted, local_branches)


if __name__ == "__main__":
    topo_order_commits()
