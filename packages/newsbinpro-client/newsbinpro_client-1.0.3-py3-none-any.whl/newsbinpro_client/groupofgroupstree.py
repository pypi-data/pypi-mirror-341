class GroupOfGroupsTree:
    """
    Represents a tree structure to manage groups of groups.

    Methods:
        __init__:
            Initializes an instance of the GroupOfGroupsTree class.

        group_of_group_names:
            Property that returns the names of all the groups of groups.

        get_group_of_groups_children:
            Retrieves the children (group names) associated with a specific group of groups name.

        add:
            Adds a new group name under a specific group of groups name.
    """

    def __init__(self):
        """
        Initializes an instance of the class.

        This constructor creates an empty dictionary `group_of_groups` which can be
        used to store hierarchical group structures or other related hierarchical
        data. Each key in the dictionary can represent a group name or identifier, and
        each value can represent nested groups or associated data.
        """
        self.group_of_groups = {}

    @property
    def group_of_group_names(self):
        """
        :return: A sequence of group names representing the keys of the group_of_groups dictionary.
        """
        return self.group_of_groups.keys()

    def get_group_of_groups_children(self, group_of_group_name: str) -> list:
        """
        :param group_of_group_name: The name of the group of groups whose children groups are to be retrieved.
        :return: A list of child groups associated with the specified group of groups, or an empty list if no children exist.
        """
        return self.group_of_groups.get(group_of_group_name, [])

    def add(self, group_of_groups_name: str, group_name: str) -> None:
        """
        :param group_of_groups_name: The name of the group of groups where the new group will be added.
        :param group_name: The name of the group to be added to the specified group of groups.
        :return: None
        """
        if group_of_groups_name not in self.group_of_groups:
            self.group_of_groups[group_of_groups_name] = []
        self.group_of_groups[group_of_groups_name].append(group_name)
