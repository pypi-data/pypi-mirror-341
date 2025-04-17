import logging

import pandas as pd
import numpy as np
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

from coral.utility import replace_special_with_dot


class Coral:
    def __init__(self):
        """
        Initialize the Coral class with default attributes.
        """
        self.df: pd.DataFrame | None = None
        self.unprocessed_df: pd.DataFrame | None = None
        self.conditions: list[str] = []
        self.samples: list[str] = []
        self.comparison_dict: dict[str, list[str]] = {}
        self.sample_condition_dict: dict[str, str] = {}
        self.qfeat = importr("QFeatures")
        self.limma = importr("limma")
        self.r_unprocessed_df = None
        self.q_object = None
        self.current_assay_name = ""
        self.index_columns = []
        self.design = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.r_unprocessed_df = None
        self.q_object = None
        self.design = None
        ro.r('gc()')

    def load_unproccessed_file(self, file_path: str, sep: str = "\t"):
        """
        Load an unprocessed file into a pandas DataFrame and convert it to an R DataFrame.

        :param file_path: Path to the unprocessed file.
        :param sep: Separator used in the file.
        """
        self.unprocessed_df = pd.read_csv(file_path, sep=sep,
                                          na_values=["NA", "NaN", "N/A", "#VALUE!"])
        with (ro.default_converter + pandas2ri.converter).context():
            self.r_unprocessed_df = ro.conversion.get_conversion().py2rpy(self.unprocessed_df)

    def add_condition(self, condition: str):
        """
        Add a condition to the conditions list.

        :param condition: Condition to be added.
        """
        if condition not in self.conditions:
            self.conditions.append(condition)
        else:
            logging.warning(f"Condition {condition} already in conditions")

    def add_sample(self, sample: str):
        """
        Add a sample to the samples list.

        :param sample: Sample to be added.
        """
        if sample not in self.samples:
            self.samples.append(sample)
        else:
            logging.warning(f"Sample {sample} already in samples")

    def add_condition_map(self, condition: str, samples: list[str]):
        """
        Map samples to a condition.

        :param condition: Condition to be mapped.
        :param samples: List of samples to be mapped to the condition.
        """
        if condition not in self.conditions:
            raise ValueError(f"Condition '{condition}' not found in conditions")

        for s in samples:
            if s not in self.samples:
                logging.warning(f"Sample {s} not found in samples")
            self.sample_condition_dict[s] = condition

    def add_comparison(self, condition_A: str, condition_B: str, comparison_lable: str | None = None):
        """
        Add a comparison between two conditions.

        :param condition_A: First condition.
        :param condition_B: Second condition.
        :param comparison_lable: Label for the comparison.
        """
        if condition_A not in self.conditions or condition_B not in self.conditions:
            raise ValueError(f"Condition {condition_A} or {condition_B} not found in conditions")
        if not comparison_lable:
            comparison_lable = f"{condition_A}-{condition_B}"
        self.comparison_dict[comparison_lable] = [condition_A, condition_B]

    def prepare(self):
        """
        Prepare the data for analysis by converting it to an R QFeatures object.
        """
        logging.info("Preparing data for analysis...")
        assert type(self.unprocessed_df) is pd.DataFrame
        assert self.r_unprocessed_df is not None
        assert len(self.conditions) > 0
        assert len(self.samples) > 0
        assert self.sample_condition_dict
        sample_columns_index = [n + 1 for n, c in enumerate(self.unprocessed_df.columns) if c in self.samples]
        conditions = []
        samples = []
        index_columns = []
        for c in self.index_columns:
            if c in self.unprocessed_df.columns.values:
                col = replace_special_with_dot(c)
                if col[0].isdigit():
                    col = f"X{col}"
                index_columns.append(col)

        for c in self.unprocessed_df.columns:
            if c in self.samples and c in self.sample_condition_dict:
                cond = replace_special_with_dot(self.sample_condition_dict[c])
                if cond[0].isdigit():
                    cond = f"X{cond}"
                conditions.append(cond)
                samples.append(replace_special_with_dot(c))

        r_sample_columns_index = ro.IntVector(sample_columns_index)
        ro.globalenv["conditions"] = ro.StrVector(conditions)
        ro.globalenv["samples"] = ro.StrVector(samples)
        ro.globalenv["indexColumn"] = ro.StrVector(index_columns)
        self.q_object = self.qfeat.readQFeatures(self.r_unprocessed_df, ecol=r_sample_columns_index, name='startingDF')
        ro.globalenv["data"] = self.q_object
        r_script = f"""
        data$group <- conditions
        data$sample <- samples
        currentAssayName <- 'startingDF'
        data <- selectRowData(data, indexColumn)"""
        ro.r(r_script)
        self.current_assay_name = "startingDF"
        logging.info("Data preparation complete. QFeatures object created.")
        return self

    def impute(self, method: str = "knn"):
        """
        Impute missing values in the data.

        :param method: Imputation method to be used.
        """
        r_script = f"""
        print(data)
        data <- impute(data, method = "{method}", i ="startingDF")
        currentAssayName <- "imputedAssay"
        """
        ro.r(r_script)
        self.current_assay_name = "imputedAssay"
        return self

    def filter_missing_columns(self, threshold: float = 0.7):
        """
        Filter out columns where more than a threshold of the values are missing.

        :param threshold: Threshold for filtering columns.
        """
        assert type(self.unprocessed_df) is pd.DataFrame
        keep_columns = []
        for c in self.unprocessed_df.columns:
            if c in self.sample_condition_dict:
                # count NA values
                count_na = self.unprocessed_df[c].isna().sum()
                # calculate percentage of NA values
                percentage_na = count_na / len(self.unprocessed_df.index)
                if percentage_na < threshold:
                    keep_columns.append(c)
            else:
                keep_columns.append(c)
        self.unprocessed_df = self.unprocessed_df[keep_columns]
        return self

    def filter_missing_rows(self, threshold: float = 0.7):
        """
        Filter out rows where more than a threshold of the values are missing.

        :param threshold: Threshold for filtering rows.
        """
        assert self.q_object is not None
        r_script = f"""
        data <- zeroIsNA(data, i = seq_along(data))
        data <- filterNA(data, i = seq_along(data), pNA = {threshold})
        """
        ro.r(r_script)
        return self

    def log_transform(self):
        """
        Log transform the data.
        """
        r_script = f"""
        data <- addAssay(data, logTransform(data[[seq_along(data)[length(seq_along(data))]]]), name="log2")
        currentAssayName <- "log2"
        """
        ro.r(r_script)
        self.current_assay_name = "log2"
        return self

    def normalize(self, method: str = "quantiles.robust"):
        """
        Normalize the data.

        :param method: Normalization method to be used.
        """
        valid_methods = ["quantiles", "quantiles.robust", "vsn", "center.median", "center.mean"]
        if method not in valid_methods:
            raise ValueError(f"Method '{method}' not valid. Choose from {valid_methods}")
        r_script = f"""
        data <- addAssay(data, normalize(data[[seq_along(data)[length(seq_along(data))]]], method="{method}"), name="norm")
        currentAssayName <- "norm"
        """
        ro.r(r_script)
        self.current_assay_name = "norm"
        return self

    def aggregate_features(self, feature_column: str, method: str = "MsCoreUtils::robustSummary"):
        """
        Aggregate features in the data.

        :param feature_column: Column to be used for aggregation.
        :param method: Aggregation method to be used.
        """
        assert feature_column in self.index_columns
        feature_column = replace_special_with_dot(feature_column)
        if feature_column[0].isdigit():
            feature_column = f"X{feature_column}"
        r_script = f"""
        data <- aggregateFeatures(data, i = currentAssayName, fcol = "{feature_column}", name = "aggregated", fun={method})
        currentAssayName <- "aggregated"
        """
        ro.r(r_script)
        self.current_assay_name = "aggregated"
        return self

    def prepare_for_limma(self):
        """
        Prepare data for limma analysis.
        """
        r_script = f"""
        design <- model.matrix(~0+data$group)
        colnames(design) <- gsub("data\\\\$group", "", colnames(design))
        fit <- lmFit(assay(data, currentAssayName), design)
        """
        ro.r(r_script)
        self.design = ro.r("design")
        self.current_assay_name = "limma"
        return self

    def run_limma(self):
        """
        Run limma analysis on the data.
        """
        assert self.design is not None
        assert self.comparison_dict
        for comp in self.comparison_dict:
            condition_A = replace_special_with_dot(self.comparison_dict[comp][0])
            if condition_A[0].isdigit():
                condition_A = f"X{condition_A}"
            condition_B = replace_special_with_dot(self.comparison_dict[comp][1])
            if condition_B[0].isdigit():
                condition_B = f"X{condition_B}"

            contrast_matrix = self.limma.makeContrasts(contrast1=f"{condition_A}-{condition_B}", levels=self.design)
            ro.globalenv["contrast.matrix"] = contrast_matrix
            r_script = f"""
            fit2 <- contrasts.fit(fit, contrast.matrix)
            fit2 <- eBayes(fit2)
            result <- topTable(fit2, coef=1, adjust="BH", number=Inf, sort.by="none")
            result <- cbind(as.data.frame(rowData(data[[currentAssayName]])), result)
            """
            ro.r(r_script)
            result = ro.r("result")
            with (ro.default_converter + pandas2ri.converter).context():
                pd_from_r_df = ro.conversion.get_conversion().rpy2py(result)
                pd_from_r_df["comparison"] = comp
                yield pd_from_r_df

    def export_df_from_R(self, file_path: str, sep: str = "\t"):
        """
        Export the current R DataFrame to a file.

        :param file_path: Path to the output file.
        :param sep: Separator to be used in the output file.
        """
        r_script = f"""
        tempt.df <- cbind(as.data.frame(rowData(data[[currentAssayName]])), assay(data, currentAssayName))
        write.table(tempt.df, file="{file_path}", sep="{sep}", row.names=TRUE, col.names=TRUE, quote=FALSE)
        """
        ro.r(r_script)

    def get_current_assay_as_dataframe(self) -> pd.DataFrame:
        """Get the current assay as a pandas DataFrame."""
        r_script = f"""
        temp_df <- cbind(as.data.frame(rowData(data[[currentAssayName]])), 
                        assay(data, currentAssayName))
        """
        ro.r(r_script)
        with (ro.default_converter + pandas2ri.converter).context():
            return ro.conversion.get_conversion().rpy2py(ro.r("temp_df"))

    @property
    def index_columns(self):
        return self._index_columns

    @index_columns.setter
    def index_columns(self, columns):
        if self.unprocessed_df is not None:
            for col in columns:
                if col not in self.unprocessed_df.columns:
                    logging.warning(f"Column '{col}' not found in data")
        self._index_columns = columns

    def reset(self):
        """
        Reset the Coral object to its initial state, clearing all data and settings.

        This method cleans up R objects, clears all stored data, and resets all
        settings to their default values, effectively returning the object to
        the state it was in after initialization.

        :return: self for method chaining
        """
        self.r_unprocessed_df = None
        self.q_object = None
        self.design = None
        ro.r('gc()')

        self.df = None
        self.unprocessed_df = None

        self.conditions = []
        self.samples = []
        self.comparison_dict = {}
        self.sample_condition_dict = {}

        self.current_assay_name = ""
        self._index_columns = []

        self.qfeat = importr("QFeatures")
        self.limma = importr("limma")

        logging.info("Coral object has been reset to initial state")
        return self







