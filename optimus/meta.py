from glom import glom, assign

from optimus.helpers.core import val_to_list


def meta(self):
    """
    Functions to handle dataFrames metadata
    Actions are operations like rename col, copy col... all the functions in columns.py. This used to track
    what should be recalculated in the profiler. For example a copy or rename operation do not need to
    fire a column profiling
    """
    df_self = self

    class Meta:
        @staticmethod
        def reset(self):
            df = self.meta.set("transformations.actions", [])
            # Profiler.instance.output_columns = {}
            return df

        @staticmethod
        def append_action(key, action, value):
            df = self
            old_value = df.meta.get(key)
            old_value.append({action: value})
            df = df.meta.set(key, old_value)
            return df

        @staticmethod
        def copy(old_new_columns):
            """
            Shortcut to add copy transformations to a dataframe
            :param old_new_columns:
            :return:
            """

            key = "transformations.actions"

            df = self
            df = df.meta.append_action(key, "copy", old_new_columns)

            return df

        @staticmethod
        def rename(old_new_columns):
            """
            Shortcut to add rename transformations to a dataframe
            :param old_new_columns:
            :return:
            """

            key = "transformations.actions"

            df = self
            df = df.meta.append_action(key, "rename", old_new_columns)

            return df

        @staticmethod
        def columns(value):
            """
            Shortcut to cache the columns in a dataframe
            :param value:
            :return:
            """
            df = self
            value = val_to_list(value)
            for v in value:
                df = df.meta.update("transformations.columns", v, list)
            return df

        @staticmethod
        def action(name, value):
            """
            Shortcut to add actions to a dataframe
            :param name:
            :param value:
            :return:
            """
            key = "transformations.actions"

            df = self
            df = df.meta.append_action(key, name, value)

            return df

        @staticmethod
        def preserve(old_df, key=None, value=None):
            """
            In some cases we need to preserve metadata actions before a destructive dataframe transformation.
            :param old_df: The Spark dataframe you want to copy the metadata
            :param key:
            :param value:
            :return:
            """
            old_meta = old_df.meta.get()
            new_meta = self.meta.get()

            new_meta.update(old_meta)
            if key is None or value is None:
                return self.meta.set(value=new_meta)
            else:

                return self.meta.set(value=new_meta).meta.action(key, value)

        @staticmethod
        def update(path, value, default=list):
            """
            Update meta data in a key
            :param path:
            :param value:
            :param default:
            :return:
            """

            df = df_self

            new_meta = df.meta.get()
            if new_meta is None:
                new_meta = {}

            elements = path.split(".")
            result = new_meta
            for i, ele in enumerate(elements):
                if ele not in result and not len(elements) - 1 == i:
                    result[ele] = {}

                if len(elements) - 1 == i:
                    if default is list:
                        result.setdefault(ele, []).append(value)
                    elif default is dict:
                        result.setdefault(ele, {}).update(value)
                else:
                    result = result[ele]

            df = df.meta.set(value=new_meta)
            return df

        @staticmethod
        def set(spec=None, value=None, missing=dict):
            """
            Set metadata in a dataframe columns
            :param spec: path to the key to be modified
            :param value: dict value
            :param missing:
            :return:
            """
            if spec is not None:
                target = self.meta.get()
                data = assign(target, spec, value, missing=missing)
            else:
                data = value

            df = self
            df.schema[-1].metadata = data
            return df

        @staticmethod
        def get(spec=None):
            """
            Get metadata from a dataframe column
            :param spec: path to the key to be modified
            :return:
            """
            data = self.schema[-1].metadata
            if spec is not None:
                data = glom(data, spec, skip_exc=KeyError)
            return data

    return Meta()
