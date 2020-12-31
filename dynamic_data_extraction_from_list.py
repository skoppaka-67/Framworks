def creat_conditional_block(self, line_list, ):
    IF_VAR = "If"
    ELSE_VAR = "Else "
    END_IF_VAR = "End If"
    ELSE_IF_VAR = "ElseIf"

    #
    index_list = []

    for index, line in enumerate(line_list):
        if line.strip().startswith(IF_VAR):
            # print("IF" ,line,index)
            index_list.append({IF_VAR: index})

        if line.strip().startswith(ELSE_VAR):
            index_list.append({ELSE_VAR: index})

        if line.strip().startswith(ELSE_IF_VAR):
            index_list.append({ELSE_IF_VAR.strip(): index})

        if re.search('.*' + END_IF_VAR + '.*', line):
            # print("END --->", line_list[index],index)
            index_list.append({END_IF_VAR: index})

    # print(json.dumps(index_list, indent=4))

    stnd_list = []
    pop_list = []

    for index, iter in enumerate(index_list):

        alter_index = index + 1

        if (IF_VAR in index_list[index] and IF_VAR in index_list[alter_index]) or (
                IF_VAR in index_list[index] and ELSE_VAR in index_list[alter_index]) or (
                IF_VAR in index_list[index] and ELSE_IF_VAR in index_list[alter_index]):
            block_counter = block_counter + 1
            stnd_list.append(block_counter)
            pop_list.append(block_counter)
            total_if_block_counter = total_if_block_counter + 1

            # print(f'Cond:{stnd_list[-1]}', line_list[list(index_list[index].values())[0]])

            conditional_block_var = line_list[list(index_list[index].values())[0]]
            node_sequence.append('C' + str(total_if_block_counter))

            node_code['C' + str(total_if_block_counter)] = conditional_block_var

            # print(f"TRUE-BLOCK:{stnd_list[-1]}",line_list[list(index_list[index].values())[0] + 1: list(index_list[alter_index].values())[0]])

            true_block_var = line_list[
                             list(index_list[index].values())[0] + 1: list(index_list[alter_index].values())[0]]

            node_sequence.append('T' + str(stnd_list[-1]))

            node_code['T' + str(stnd_list[-1])] = true_block_var

            true_block_var = ''
            conditional_block_var = ''

        if IF_VAR in index_list[index] and END_IF_VAR in index_list[alter_index]:
            block_counter = block_counter + 1
            stnd_list.append(block_counter)
            pop_list.append(block_counter)
            total_if_block_counter = total_if_block_counter + 1

            # print(f'Cond:{stnd_list[-1]}', line_list[list(index_list[index].values())[0]])
            conditional_block_var = line_list[list(index_list[index].values())[0]]
            node_sequence.append('C' + str(total_if_block_counter))

            node_code['C' + str(total_if_block_counter)] = conditional_block_var

            conditional_block_var = ''

            # print(f"TRUE-BLOCK:{stnd_list[-1]}",
            #       line_list[list(index_list[index].values())[0] + 1: list(index_list[alter_index].values())[0]])

            true_block_var = line_list[
                             list(index_list[index].values())[0] + 1: list(index_list[alter_index].values())[0]]
            node_sequence.append('T' + str(stnd_list[-1]))

            node_code['T' + str(stnd_list[-1])] = true_block_var
            true_block_var = ''
            false_block_count = pop_list.pop()
            print(f"FALSE-BLOCK:{false_block_count}", [])
            node_sequence.append("F" + str(false_block_count))
            node_code['F' + str(false_block_count)] = []

        if (ELSE_VAR in index_list[index] and IF_VAR in index_list[alter_index]) or (
                ELSE_VAR in index_list[index] and END_IF_VAR in index_list[alter_index]) or (
                ELSE_IF_VAR in index_list[index] and ELSE_IF_VAR in index_list[alter_index]) or (
                ELSE_IF_VAR in index_list[index] and ELSE_VAR in index_list[alter_index]):
            false_block_var = line_list[
                              list(index_list[index].values())[0] + 1: list(index_list[alter_index].values())[0]]

            # print(f"FALSE-BLOCK:{pop_list.pop()}", [])
            false_block_count = pop_list.pop()
            node_sequence.append("F" + str(false_block_count))
            node_code['F' + str(false_block_count)] = false_block_var
            false_block_var = ''

            # print(f"FALSE-BLOCK:{pop_list.pop()}",
            #       line_list[list(index_list[index].values())[0] + 1: list(index_list[alter_index].values())[0]])

        if alter_index < len(index_list):
            if (END_IF_VAR in index_list[index] and END_IF_VAR in index_list[alter_index]) or (
                    END_IF_VAR in index_list[index] and ELSE_IF_VAR in index_list[alter_index]) or (
                    END_IF_VAR in index_list[index] and ELSE_VAR in index_list[alter_index]):

                if list(index_list[index].values())[0] + 1 == list(index_list[alter_index].values())[0]:
                    continue
                else:
                    print(f"Group-BLOCK:{block_counter}", )
                    group_block_variable = " ".join(
                        line_list[
                        list(index_list[index].values())[0] + 1: list(index_list[alter_index].values())[0]])
                    total_group_block_counter = total_group_block_counter + 1
                    node_sequence.append('G' + str(total_group_block_counter))

                    node_code['G' + str(total_group_block_counter)] = group_block_variable
                    group_block_variable = ''

    return True, total_group_block_counter, block_counter, node_sequence, node_code, total_if_block_counter
