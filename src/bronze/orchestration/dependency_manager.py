"""
Gerenciamento de dependências entre datasets.
"""

def sort_datasets_by_dependency(
    datasets_config: dict
) -> list:

    ordered = []

    remaining = dict(
        datasets_config
    )

    while remaining:

        progress = False

        for dataset_name, config in list(
            remaining.items()
        ):

            dependency = config.get(
                "dependency"
            )

            if (

                not dependency

                or

                dependency["parent"]

                in [

                    name
                    for name, _ in ordered
                ]
            ):

                ordered.append(
                    (
                        dataset_name,
                        config
                    )
                )

                del remaining[
                    dataset_name
                ]

                progress = True

        if not progress:

            raise RuntimeError(
                "Dependência circular detectada."
            )

    return ordered