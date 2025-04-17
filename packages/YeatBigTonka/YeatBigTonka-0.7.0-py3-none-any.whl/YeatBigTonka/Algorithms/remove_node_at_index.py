class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def remove_node_at_index(head: ListNode, idx: int) -> ListNode:
    """
    Удаляет элемент с индексом idx из односвязного списка,
    начиная считать с 0.
    Возвращает новую голову списка.
    """
    # Если список пуст или индекс отрицательный - просто возвращаем head
    if not head or idx < 0:
        return head

    # Если надо удалить самый первый элемент
    if idx == 0:
        return head.next  # возвращаем голову, сместив на следующий узел

    current = head
    current_index = 0

    # Находим узел, идущий перед тем, который нужно удалить
    while current and current_index < idx - 1:
        current = current.next
        current_index += 1

    # Если мы дошли до нужного места и у следующего узла существует элемент
    if current and current.next:
        # "Пропускаем" узел по индексу idx
        current.next = current.next.next

    return head
