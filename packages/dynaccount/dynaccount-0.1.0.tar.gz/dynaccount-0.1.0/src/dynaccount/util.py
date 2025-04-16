import re

def format_bound_groups(policy):
    bound_groups_set = set()
    
    for binding_type in policy.get('bindings', {}):
        for binding in policy['bindings'][binding_type].get('policyBindings', []):
            for group in binding.get("groups", []):
                bound_groups_set.add(group['name'])

    bound_groups = '; '.join(bound_groups_set)
    return bound_groups

def enrich_policies_with_groups(policies, groups):
    # Create a dictionary to quickly look up groups by their uuid
    group_dict = {group['uuid']: group for group in groups}

    # Enrich policies with group information
    for policy in policies:
        if 'bindings' in policy and policy['bindings']:
            for binding_type in policy['bindings'].keys():
                for binding in policy['bindings'][binding_type]['policyBindings']:
                    enriched_groups = []
                    for group_uuid in binding['groups']:
                        if group_uuid in group_dict:
                            enriched_groups.append(group_dict[group_uuid])
                    binding['groups'] = enriched_groups

    return policies

def get_policies_detailed(interface, search, regex=False):
    all_account_policies_detailed = []

    for policy in interface.account_policies:
        policy_detailed = {'bindings': {}, 'details': interface.get_policy_details(policy['levelType'], policy['levelId'], policy['uuid'])}
        policy_match = False

        if regex:
            pattern = re.compile(search)
            if pattern.search(policy_detailed['details']['statementQuery']):
                policy_match = True
        else:
            if search in policy_detailed['details']['statementQuery']:
                policy_match = True

        if policy_match:
            policy_detailed['bindings']['account'] = interface.get_policy_bindings('account', interface.account_uuid, policy['uuid'])

            for env in interface.environments:
                env_id = env['id']
                policy_detailed['bindings'][env_id] = interface.get_policy_bindings('environment', env_id, policy['uuid'])

            all_account_policies_detailed.append(policy_detailed)

    return all_account_policies_detailed